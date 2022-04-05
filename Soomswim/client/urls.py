from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
]   