from django.db import models
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 20)
    usermail = models.EmailField()
    userpass = models.CharField(max_length = 20,null = False)
    enabled = models.BooleanField(default = False)
    def __str__(self):
        return self.name
class Topic(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    topic = models.CharField(max_length = 20)
    topic_time = models.DateTimeField(auto_now_add=1)
    def __str__(self):
        return self.topic
class Content(models.Model):
    title = models.ForeignKey(Topic,on_delete=models.CASCADE)
    content = models.TextField()
    content_time = models.DateTimeField(auto_now_add=1)
    def __str__(self):
        return self.content[:50]
