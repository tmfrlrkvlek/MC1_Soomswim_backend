from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
import requests
from datetime import datetime, timedelta
from django.db.models import Q
from django.core import serializers
from django.forms.models import model_to_dict

AVAILABLE_TIME = 8

# Create your views here.
@api_view(['POST'])
def login(request) :
    id = request.data['name']
    if AppUser.objects.filter(name = id).exists() : 
        return JsonResponse({'code':200, 'message':'login complete'}, status=200)
    else :
        user = AppUser()
        user.name = id
        user.save()
        return JsonResponse({'code':201, 'message': 'sign up complete'}, status=201)

@api_view(['POST'])
def uploadStory(request) :
    content = request.data['content']
    user = AppUser.objects.get(name = request.data['writer'])
    if len(content) > 5000 : 
        return JsonResponse({'code':422, 'message': 'too long contents'}, status=422)
    else :
        story = Story()
        story.content = content
        story.writer = user
        story.save()
        return JsonResponse({'code':201, 'message': 'story upload complete'}, status=201)

@api_view(['GET'])
def story(request) :
    user = AppUser.objects.get(name = request.GET['name'])
    story = Story.objects.get(id=request.GET['story'])
    data = model_to_dict(story)
    date = data['date']
    data['date'] = datetime.strftime(date, '%Y.%m.%d %l:%M %p')
    data['writer'] = model_to_dict(story.writer, fields = ['id', 'name'])
    data['writer']['profile'] = ''
    data['reply_check_permission'] = date <= datetime.now() - timedelta(hours=AVAILABLE_TIME)
    remaining_time = 0 if data['reply_check_permission'] else date + timedelta(hours=AVAILABLE_TIME) - datetime.now() 
    if remaining_time == 0 :
        data['remaining_time'] = None
    else :
        remaining_time = str(remaining_time).split(':')
        data['remaining_time'] = '{}시간 {}분 남음'.format(remaining_time[0], remaining_time[1]) if remaining_time[0] != '0' else '{}분 남음'.format(remaining_time[1])         
    if story.writer == user :
        data['reply_availability'] = False
        data['reply_existence'] = False
    else : 
        data['reply_availability'] = story.date > datetime.now() - timedelta(hours=AVAILABLE_TIME)
        data['reply_existence'] = Reply.objects.filter(writer = user, story = story).exists()
        data['reply_check_permission'] = False
    return JsonResponse({'data': data, 'code': 200, 'message': 'get story complete'}, status=200)

@api_view(['GET'])
def stories(request) :
    user = AppUser.objects.get(name = request.GET['name'])
    relations = Relationship.objects.filter(Q(receiver = user)|Q(requester = user), state = 1)
    writers = [user]
    [writers.append(relation.requester if relation.requester != user else relation.receiver) for relation in relations]
    end_time = datetime.now() - timedelta(hours=AVAILABLE_TIME)
    stories = Story.objects.filter(writer__in = writers, date__gte=end_time).order_by('-date').values('id', 'date', 'content', 'writer_id')
    if stories.exists() :
        data = []
        for story in stories :
            story['writer'] = AppUser.objects.filter(id = story['writer_id']).values('id', 'name', 'profile')[0]
            story['date'] = datetime.strftime(story['date'], '%Y.%m.%d %l:%M %p')
            story['content'] = story['content'][:150]
            del story['writer_id']
            data.append(story)
        return JsonResponse({'data': data, 'code': 200, 'message': 'get story complete'}, status=200)
    else :
        return JsonResponse({'data': [], 'code': 204, 'message': 'no contents'}, status=204)

@api_view(['POST'])
def reply(request) :
    if len(request.data['content']) > 5000 : 
        return JsonResponse({'code':422, 'message': 'too long reply contents'}, status=422)
    elif len(request.data['writer']) > 30 : 
        return JsonResponse({'code':422, 'message': 'too long writer nickname'}, status=422)
    else : 
        reply = Reply()
        reply.content = request.data['content']
        reply.sender = AppUser.objects.get(name = request.data['sender'])
        reply.writer = request.data['writer']
        reply.story = Story.objects.get(id=request.data['story'])
        reply.save()
        return JsonResponse({'code':201, 'message': 'reply upload complete'}, status=201)

@api_view(['GET'])
def mystories(request) :
    user = AppUser.objects.get(name = request.GET['name'])
    stories = Story.objects.filter(writer = user).order_by('-date').values('id', 'date', 'content', 'writer_id')
    if stories.exists() :
        data = []
        for story in stories :
            story['writer'] = AppUser.objects.filter(id = story['writer_id']).values('id', 'name', 'profile')[0]
            date = story['date']
            story['date'] = datetime.strftime(date, '%Y.%m.%d %l:%M %p')
            story['content'] = story['content'][:30]
            story['reply_check_permission'] = date <= datetime.now() - timedelta(hours=AVAILABLE_TIME)
            remaining_time = 0 if story['reply_check_permission'] else date + timedelta(hours=AVAILABLE_TIME) - datetime.now() 
            if remaining_time == 0 :
                story['remaining_time'] = None
            else :
                remaining_time = str(remaining_time).split(':')
                story['remaining_time'] = '{}시간 {}분 남음'.format(remaining_time[0], remaining_time[1]) if remaining_time[0] != '0' else '{}분 남음'.format(remaining_time[1]) 
            del story['writer_id']
            data.append(story)
        return JsonResponse({'data': data, 'code': 200, 'message': 'get stories complete'}, status=200)
    else :
        return JsonResponse({'code': 204, 'message': 'no contents'}, status=204)

@api_view(['POST'])
def friendRequest(request) :
    user = AppUser.objects.get(name = request.data['name'])
    friend = AppUser.objects.get(id = request.data['friend'])
    if Relationship.objects.filter(requester = user, receiver = friend).exists() or Relationship.objects.filter(requester = friend, receiver = user).exists() :
        return JsonResponse({'code':202, 'message': 'already exists request'}, status=202)
    else :
        relationship = Relationship()
        relationship.requester = AppUser.objects.get(name = request.data['name'])
        relationship.receiver = AppUser.objects.get(id = request.data['friend'])
        relationship.save()
        return JsonResponse({'code':201, 'message': 'request complete'}, status=201)

@api_view(['POST'])
def friendResponse(request) :
    user = AppUser.objects.get(name = request.data['name'])
    friend = AppUser.objects.get(id = request.data['friend'])
    relation = Relationship.objects.filter(requester = friend, receiver = user, state = 0)
    if relation.exists() :
        relation = relation[0]
        relation.state = 1 if request.data['response'] else 2
        relation.save()
        return JsonResponse({'code': 200, 'message': 'request complete'}, status = 200)
    else :
        return JsonResponse({'code': 202, 'message': 'nonexistent request'}, status=202)
    

@api_view(['GET'])
def friends(request) :
    user = AppUser.objects.get(name = request.GET['name'])
    relations = Relationship.objects.filter(Q(receiver = user)|Q(requester = user), state = 1)
    if relations.exists() :
        friends = []
        for relation in relations :
            friend = model_to_dict(relation.requester if relation.requester != user else relation.receiver, ['id', 'name'])
            friend['profile'] = ''
            friends.append(friend)
        return JsonResponse({'data': friends, 'code': 200, 'message': 'get friends complete'}, status=200)
    else :
        return JsonResponse({'code': 204, 'message': 'no friends'}, status=204)

@api_view(['GET'])
def replies(request) :
    user = AppUser.objects.get(name = request.GET['name'])
    story = Story.objects.get(id = request.GET['story'])
    if story.writer != user :
        return JsonResponse({'code': 401, 'message': 'unauthorized request'}, status=401)
    elif story.date > datetime.now() - timedelta(hours=AVAILABLE_TIME) :
        return JsonResponse({'code': 403, 'message': 'Forbidden request'}, status=403)
    else :
        replies = Reply.objects.filter(story = story)
        if replies.exists() :
            return JsonResponse({'data': {'id_list': [reply.id for reply in replies], 'count': len(replies) },'code': 200, 'message': 'get replies complete'}, status=200)
        else :
            return JsonResponse({'code': 204, 'message': 'no replies'}, status=204)

@api_view(['GET'])
def readReply(request) :
    reply = Reply.objects.get(id = request.GET['reply'])
    data = model_to_dict(reply, fields=['id', 'content', 'writer'])
    data['date'] = datetime.strftime(reply.date, '%Y.%m.%d %l:%M %p')
    return JsonResponse({'data': data,'code': 200, 'message': 'get reply complete'}, status=200)

