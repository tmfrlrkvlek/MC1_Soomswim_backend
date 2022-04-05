from .models import *
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
import requests

# Create your views here.
@api_view(['POST'])
def login(request) :
    id = request.data['id']
    if AppUser.objects.filter(name = id).exists() : 
        return JsonResponse({'code':200, 'message':'login complete'}, status=200)
    else :
        user = AppUser()
        user.name = id
        user.save()
        return JsonResponse({'code':201, 'message': 'sign up complete'}, status=201)

@api_view(['POST'])
def createStory(request) :
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
