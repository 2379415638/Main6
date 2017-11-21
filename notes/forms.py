from django import forms
from . import models
class contentform(forms.ModelForm):
    class Meta:
        model = models.Content
        fields = ['content',]
        labels = {'content': "Write your content:"}
        widgets = {'content':forms.Textarea(attrs = {'cols': 185,'rows':25})}
class topicform(forms.ModelForm):
    class Meta:
        model = models.Topic
        fields = ['topic',]
        labels = {'topic':"Create your topic:",}