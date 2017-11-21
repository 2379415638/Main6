from django.shortcuts import render,HttpResponse
from datetime import datetime
from notes import models
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from . import forms
# Create your views here.
def time(request):
    time = datetime.now()
    context = {'time':time}
    return render(request,'time.html',context)
def index(request):
    years = range(1990,2010)
    time = datetime.now()
    context = {'time':time,'years':years}
    return render(request,"index.html",context)
def Topic(request):
    time = datetime.now()
    topics = models.Topic.objects.all().order_by('topic_time')
    context = {'time':time,'topics':topics}
    return render(request,'Topic.html',context)
def topic(request,id):
    time = datetime.now()
    topic = models.Topic.objects.get(id = id)
    entries = topic.content_set.order_by('content_time')
    context ={'time':time,'topic':topic,'entries':entries}
    return render(request,'topics.html',context)
def entry(request,topic_id,entry_id):
    time = datetime.now()
    topic = models.Topic.objects.get(id = topic_id)
    entry = topic.content_set.get(id = entry_id)
    context = {'time':time,'topic':topic,'entry':entry}
    return render(request,'entry.html',context)
def user(request):
    time =datetime.now()
    identity = False
    id = None
    password = None
    try:
        id = request.GET['user_id']
        password = request.GET['user_password']
        if (id == "2379415638" and password == "lsrq.0218"):
            identity = True
    except:
        pass
    context = {'time':time,'id':id,'identity':identity,'password':password}
    return render(request,'user.html',context)
def create_topic(request):
    time = datetime.now()
    check = None
    if request.method == 'POST':
        form = forms.topicform(request.POST)
        if form.is_valid():
            topic = form.save(commit = 0)
            topic.topic_time = time
            topic.save()
            return HttpResponseRedirect(reverse('notes:Topic'))
        else:
            check  = "Wrong form!"
    else:
        form = forms.topicform()
    context = {'time':time,'check':check,'form':form}
    return render(request,'create_topic.html',context)
def del_topic(request,topic_id):
    topic = models.Topic.objects.get(id = topic_id)
    topic.delete()
    return HttpResponseRedirect(reverse("notes:Topic"))
def create_entry(request,id):
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
    context = {'form':form,'response':reponse,'time':time}

    return render(request,'create_entry.html',context)
def edit_entry(request,topic_id,entry_id):
    topic = models.Topic.objects.get(id = topic_id)
    entry = topic.content_set.get(id = entry_id)
    if request.method == 'POST':
        form = forms.contentform(instance = entry,data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("notes:entry",args = [topic_id,entry_id]))
    else:
        form = forms.contentform(instance = entry)
    context = {'form':form}
    return render(request,'edit_entry.html',context)
def del_entry(request,topic_id,entry_id):
    topic = models.Topic.objects.get(id = topic_id)
    entry = topic.content_set.get(id = entry_id)
    entry.delete()
    return HttpResponseRedirect(reverse("notes:topic",args = [topic_id]))
def personal(request):
    time = datetime.now()
    year = None
    years = range(1990,2011)
    months = range(1,13)
    days = range(1,32)
    if (request.method == 'GET'):
        try:
            year = request.GET['year']
            year = str(int(year)+18)
        except:
            pass
    context = {'years':years,'months':months,'days':days,'year':year}
    return render(request,'personal information.html',context)
