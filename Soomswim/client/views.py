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

