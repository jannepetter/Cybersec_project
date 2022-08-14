
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm
from .models import Message
import logging
import datetime

# @login_required     #broken access control. Remove comments to fix
def homeView(request, template_name="home.html"):
    users = User.objects.all()

    context = {
        'users':users,
        'sender':request.user
        
    }
    return render(request,template_name,context)

@login_required 
def messageView(request,template_name="messages.html"):

    messages= Message.objects.filter(to_user=request.user)

    context = {
        'messages':messages
    }
    return render(request,template_name,context)

@login_required 
def allMessageView(request,template_name="allmessages.html"):

    messages=Message.objects.all()
    context = {
        "messages":messages
    }
    return render(request,template_name,context)

@login_required 
def sendMessageView(request,template_name="send_message.html"):
    # Insecure design. You can change the message sender from address bar
    # Injection. Via message content, you are able to save xss to a database.

    logging.basicConfig(filename="application_logs.log", level=logging.INFO)
    
    to_user=None
    from_user=None
    if request.GET['to']:
        to_user=request.GET['to']
    if request.GET['from']:
        from_user=request.GET['from']

    form = MessageForm(request.POST, request=request, initial={'from_user':from_user,'to_user':to_user})
    send_to = User.objects.get(id=to_user)
    if form.is_valid():
        form.save()

        # security logging and monitoring failures.Remove comments to fix.
        logging.info(f"{datetime.datetime.now()} message send by {request.user}, id: {request.user.id}, from_user:{from_user}, to_user:{to_user}, content:{form.cleaned_data['content']}")

    context = {
        "form":form,
        "send_to":send_to
    }
    return render(request,template_name,context)
