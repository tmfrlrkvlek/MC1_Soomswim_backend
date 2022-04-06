from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('story', story, name='story'),
    path('mypage/story', uploadStory, name='story'),
    path('storys', storys, name='storys'),
    path('reply', reply, name='reply'),
    path('mypage/storys', mystorys, name='mystorys'),
    path('friend/request', friendRequest, name='friend/request'),
    path('friend/response', friendResponse, name='friend/response'),
    path('friends', friends, name='friends')
]   