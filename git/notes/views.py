from django.shortcuts import render,HttpResponse
from datetime import datetime
from notes import models
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from . import forms
from django.core.mail import send_mail
from captcha.fields import CaptchaField
# Create your views here.
def usernamecheck(request):
    if 'mail' in request.session:
        return request.session['mail']
    else:
        return None
def index(request):
    username = usernamecheck(request)
    time = datetime.now()
    context = {'time':time,'username':username}
    return render(request,"index.html",context)
def Topic(request):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    time = datetime.now()
    user = models.User.objects.get(usermail = request.session['mail'])
    topics = user.topic_set.order_by('topic_time')
    context = {'time':time,'topics':topics,'username':username}
    return render(request,'Topic.html',context)
def topic(request,id):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    time = datetime.now()
    topic = None
    entries = None
    try:
        topic = models.Topic.objects.get(id = id)
        entries = topic.content_set.order_by('content_time')
    except:
        pass
    context ={'time':time,'topic':topic,'entries':entries,'username':username}
    return render(request,'topics.html',context)
def entry(request,topic_id,entry_id):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    time = datetime.now()
    topic = models.Topic.objects.get(id = topic_id)
    entry = topic.content_set.get(id = entry_id)
    context = {'time':time,'topic':topic,'entry':entry,'username':username}
    return render(request,'entry.html',context)
# def user(request):
#     if request.method == 'POST':
#         form = forms.User(data = request.POST)
#         if form.is_valid():
#             id = form.cleaned_data['id']
#             password = form.cleaned_data['password']
#             response = HttpResponseRedirect(reverse("notes:index"))
#             response.set_cookie("id",id)
#             response.set_cookie("password",password)
#             return response
#     else:
#         form = forms.User()
#     context = {'form':form}
#     return render(request,'login.html',context)
def login(request):
    enabled = None
    if request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            try:
                user = models.User.objects.get(usermail = mail)
                if password == user.userpass:
                    enabled = True
                    request.session['mail'] = user.usermail
                    request.session['password'] = user.userpass
                    return HttpResponseRedirect(reverse('notes:index'))
            except:
                enabled = False
        else:
            pass
    else:
        form = forms.Login()
    context = {'form':form,'enabled':enabled}
    return render(request,'login.html',context)
def logout(request):
    request.session.delete()
    return render(request,"index.html")
def create_user(request):
    username = usernamecheck(request)
    str = ""
    if request.method == 'POST':
        form = forms.Userform(data = request.POST)
        if form.is_valid():
            if models.User.objects.filter(usermail = form.cleaned_data['usermail']).exists():
                str = "This user has been existed!"
            else:
                user = form.save(commit = 0)
                user.save()
                request.session['mail'] = user.usermail
                request.session['password'] = user.userpass
                return HttpResponseRedirect(reverse('notes:index'))
    else:
        form = forms.Userform()
    context = {'form':form,'response':str,'username':username}
    return render(request,'User.html',context)
def create_topic(request):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    time = datetime.now()
    check = None
    if request.method == 'POST':
        form = forms.topicform(request.POST)
        if form.is_valid():
            topic = form.save(commit = 0)
            topic.topic_time = time
            topic.user = models.User.objects.get(usermail = request.session['mail'])
            topic.save()
            return HttpResponseRedirect(reverse('notes:Topic'))
        else:
            check  = "Wrong form!"
    else:
        form = forms.topicform()
    context = {'time':time,'check':check,'form':form,'username':username}
    return render(request,'create_topic.html',context)
def del_topic(request,topic_id):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    topic = models.Topic.objects.get(id = topic_id)
    topic.delete()
    return HttpResponseRedirect(reverse("notes:Topic"))
def create_entry(request,id):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    time = datetime.now()
    title = models.Topic.objects.get(id = id)
    reponse = None
    if request.method == 'POST':
        form = forms.contentform(request.POST)
        if form.is_valid():
            entry = form.save(commit = 0)
            entry.title = title
            entry.save()
            return HttpResponseRedirect(reverse('notes:topic',args = [id,]))
        else:
            reponse = "Wrong form!"
    else:
        form = forms.contentform()
    context = {'form':form,'response':reponse,'time':time,'username':username}

    return render(request,'create_entry.html',context)
def edit_entry(request,topic_id,entry_id):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    topic = models.Topic.objects.get(id = topic_id)
    entry = topic.content_set.get(id = entry_id)
    if request.method == 'POST':
        form = forms.contentform(instance = entry,data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("notes:entry",args = [topic_id,entry_id]))
    else:
        form = forms.contentform(instance = entry)
    context = {'form':form,'username':username}
    return render(request,'edit_entry.html',context)
def del_entry(request,topic_id,entry_id):
    username = usernamecheck(request)
    if username == None:
        return HttpResponseRedirect(reverse('notes:login'))
    topic = models.Topic.objects.get(id = topic_id)
    entry = topic.content_set.get(id = entry_id)
    entry.delete()
    return HttpResponseRedirect(reverse("notes:topic",args = [topic_id]))
def Advice(request):
    title = "Advice"
    response = ""
    if request.method == 'POST':
        form = forms.Advice(request.POST)
        if form.is_valid():
            body = form.cleaned_data['advice']
            User = form.cleaned_data['mail']
            send_mail('Advice',body,'postmaster@seeksrq.top',[User,],fail_silently=False)
            return HttpResponseRedirect(reverse("notes:index"))
        else:
            response = "Failed"
    else:
        form = forms.Advice()
    context = {'form':form,'response':response}
    return render(request,'advice.html',context)



