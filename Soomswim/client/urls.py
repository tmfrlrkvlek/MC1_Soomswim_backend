from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('story', story, name='story'),
    path('mypage/story', uploadStory, name='story'),
    path('stories', stories, name='stories'),
    path('reply', reply, name='reply'),
    path('mypage/stories', mystories, name='mystories'),
    path('mypage/friends', myfriends, name='myfriends'),
    path('friend/request', friendRequest, name='friend/request'),
    path('friend/response', friendResponse, name='friend/response'),
    path('friends', friends, name='friends'),
    path('replies', replies, name='replies'),
    path('replies/reply', readReply, name='replies/reply')
]  