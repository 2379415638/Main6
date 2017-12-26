from django import forms
from . import models
from captcha.fields import CaptchaField
class contentform(forms.ModelForm):
    class Meta:
        model = models.Content
        fields = ['content',]
        labels = {'content': "Write your content:"}
        widgets = {'content':forms.Textarea(attrs = {'cols': 185 , 'rows':25})}
class topicform(forms.ModelForm):
    class Meta:
        model = models.Topic
        fields = ['topic',]
        widgets = {'topic':forms.TextInput()}
class Userform(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['name','usermail','userpass',]
        labels = {'name':"Name:",'usermail':"Mail:",'userpass':"Pass",}
        widgets = {'userpass':forms.PasswordInput}
class Advice(forms.Form):
    advice = forms.CharField(widget = forms.Textarea,label = "Advice:")
    mail = forms.EmailField(label = "Email:")
class Login(forms.Form):
    mail = forms.CharField(label = "Mail:")
    password = forms.CharField(widget = forms.PasswordInput,label = "Pass:")
    captcha = CaptchaField(label = "")

