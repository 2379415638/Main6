from django.db import models
# Create your models here.
class Topic(models.Model):
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