from django.db import models

# Create your models here.
class User(models.Model) :
    name = models.CharField(max_length=30)
    profile = models.FileField(upload_to='media/profile')

    def __str__(self) :
        return self.name

class Story(models.Model) :
    date = models.DateTimeField()
    text = models.TextField(max_length=5000)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Reply(models.Model)  :
    date = models.DateTimeField()
    text = models.TextField(max_length=5000)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    caller = models.CharField(max_length=30)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self) :
        return self.date + ' to ' + self.caller

class Relationship(models.Model) :
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    state = models.IntegerField(default=0) # 0: 요청 1: 수락 2: 거절