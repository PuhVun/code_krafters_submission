import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *

@csrf_exempt
def index(request):
    user  = request.user
    return render(request, "auction/index.html" ,{"user" : user})

@csrf_exempt
def Missingitems(request):
    Items = Listing.objects.order_by("-When").all()
    return JsonResponse([Item.serialize() for Item in Items] , safe=False)

def login_view(request):
    if request.method == "POST": 
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auction/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auction/login.html")


def logout_view(request):
    logout(request)
    return login_view(request)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auction/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auction/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auction/register.html")


def AddItem(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            name = request.POST["ObjName"]
            desc = request.POST["Desc"]
            image = request.FILES.get("Image")  

            f = Listing(Owner=user,Name=name,Desc=desc,Image=image)
            f.save()
            return HttpResponseRedirect(reverse("index"))
        
        return render(request , "auction/Add.html" , {"user" : user})
    else:
        return login_view(request)



def viewmessages(request):
    if request.user.is_authenticated:
        user = request.user
        messages = Messages.objects.filter(Receiver=user).order_by('-When')
        
        return JsonResponse([message.serialize() for message in messages] , safe=False)
    else:
        return login_view(request)

def messages(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "auction/Messages.html", {"user" : user})
    else:
        return login_view(request)

def MessageInDetail(request , id):
    message = Messages.objects.get(id = id)
    user = request.user
    if message.Sender == user:
        return render(request, "auction/ExpandedMessage.html" , {"user" : user , "message" : message , "REPLY" : True})
    else:
        return render(request, "auction/ExpandedMessage.html" , {"user" : user , "message" : message})

def ContactOwner(request , id):
    if request.user.is_authenticated:
        item  = Listing.objects.get(id = id)
        user = request.user
        return render(request , "auction/ContactOwner.html" , {"item": item , "user" : user})
    else:
        return login_view(request)

def SaveMessage(request):
    if request.method == "POST":
        sender = request.POST["Sender"]
        receiver = request.POST["Receiver"]
        Desc = request.POST["Desc"]
        attachment = request.FILES.get("Attachment")  
        name = request.POST["Name"]
        Sender = User.objects.get(username=sender)
        Receiver = User.objects.get(username=receiver)
        item = Listing.objects.get(Name=name)

        f = Messages(Sender=Sender,Receiver=Receiver,Message=Desc,Attachment=attachment,item=item)
        f.save()
        return HttpResponseRedirect(reverse("index"))
    
def found(request):
    if request.method == "POST":
        Id = request.POST["id"]
        Item = Listing.objects.get(id = Id)
        Item.delete()
        return HttpResponseRedirect(reverse("index"))

def Reply(request):
    if request.method == "POST":
        Id = request.POST["id"]
        message = Messages.objects.get(id = Id)
        return render(request, "auction/Reply.html" , {"message" : message })

def viewsentmessages(request):
    user = request.user
    messages = Messages.objects.filter(Sender=user).order_by('-When')
    
    return JsonResponse([message.serialize() for message in messages] , safe=False)

def sentmessages(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "auction/Sent.html", {"user" : user})
    else:
        return login_view(request)