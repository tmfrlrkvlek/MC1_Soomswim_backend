from django.db import models
from datetime import datetime

# Create your models here.
class AppUser(models.Model) :
    name = models.CharField(max_length=30)
    profile = models.FileField(upload_to='media/profile', null=True)

    def __str__(self) :
        return self.name

class Story(models.Model) :
    date = models.DateTimeField(default=datetime.now)
    content = models.TextField(max_length=5000)
    writer = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    
class Reply(models.Model)  :
    date = models.DateTimeField()
    content = models.TextField(max_length=5000)
    writer = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    caller = models.CharField(max_length=30)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self) :
        return self.date + ' to ' + self.caller

class Relationship(models.Model) :
    requester = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='requester')
    receiver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='receiver')
    state = models.IntegerField(default=0) # 0: 대기 1: 수락 2: 거절

    def __str__(self) :
        str = '요청:' + requester.name + '수신:' + receiver.name + '상태: '
        if state == 0 : return str + '대기'
        elif state == 1 : return str + '수락'
        else : return str + '거절'

