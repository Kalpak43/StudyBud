from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room, Topic, message
from .forms import RoomForm


# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},

# ]

def LoginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get("Username")
        password  = request.POST.get("Password")
        
        try:
            user = User.objects.get(username = username)
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Incorrect Password")
        except:
            messages.error(request, "User does not exist")
        
    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    context = {
        'form' : form
    }

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured')
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(id__contains = q)
        )

    room_count = rooms.count()
    topics = Topic.objects.all()
    rooom_messages = message.objects.filter(Q(room__topic__name__icontains = q))
    context = {
        'rooms' : rooms,
        'topics' : topics,
        'room_count' : room_count,
        'room_messages' : rooom_messages,
    }

    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        room_message = message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {
        'room': room,
        'room_messages' : room_messages,
        'participants' : participants,
    }

    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user' : user,
        'rooms' : rooms,
        'room_messages' : room_messages,
        'topics' : topics,
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def CreateRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('Description')
        )

        return redirect('home')

    context = {
        'form' : form,
        'topics' : topics    
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You ar not allowed here!!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('Description')
        room.save()
        return redirect('home')

    context = {
        'form' : form,
        'topics' : topics,
        'room' : room 
    }
    
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def DeleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    context = {
        'room' : room
    }
    if request.user != room.host:
        return HttpResponse("You ar not allowed here!!!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', context)

@login_required(login_url='/login')
def DeleteMessage(request, pk):
    Message =message.objects.get(id = pk)
    context = {
        'message' : Message
    }
    if request.user != Message.user:
        return HttpResponse("You ar not allowed here!!!")

    if request.method == 'POST':
        Message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', context)