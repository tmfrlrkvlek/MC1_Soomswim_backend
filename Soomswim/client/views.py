from django.http.response import JsonResponse
from .models import *
import requests

# Create your views here.
def login(request) :
    id = request.POST('id')
    if User.objects.filter(name = id).exists() : 
        return JsonResponse({'code':200, 'message':'login complete'}, status=200)
    else :
        user = User()
        user.name = id
        user.save()
        return JsonResponse({'code':201, 'message': 'sign up complete'}, status=201)

