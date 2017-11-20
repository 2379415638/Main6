from django.shortcuts import render,HttpResponse
from datetime import datetime
from notes import models
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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
    if request.method == 'POST':
        content = request.POST['topic']
        post = models.Topic.objects.create(topic = content,topic_time = time)
        post.save()
        return HttpResponseRedirect(reverse('notes:Topic'))
    context = {'time':time}
    return render(request,'create_topic.html',context)
def create_entry(request,id):
    time = datetime.now()
    title = models.Topic.objects.get(id = id)
    if request.method == 'POST':
        content = request.POST['entry']
        post = models.Content.objects.create(title = title,content = content,content_time = time)
        post.save()
        return  HttpResponseRedirect(reverse("notes:topic",args = [id]))
    context = {'time':time}
    return render(request,'create_entry.html',context)
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
