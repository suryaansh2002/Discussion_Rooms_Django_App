from pydoc import pager
from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Room, Topic, Message,User
from .forms import RoomForm,MyUserCreationForm,UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

# Create your views here.

# rooms=[{'id':1,'name':'Room 1 name'},{'id':2,'name':'Room 2 name'},{'id':3,'name':'Room 3 name'},]


def loginPage(request):
    page = 'login'
    if(request.user.is_authenticated):
        return redirect('home')
    if(request.method == 'POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect')

    return render(request, 'base/login_register.html', {'page': page})


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured in registration')

    return render(request, 'base/login_register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)

    )
    total=Room.objects.filter()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)

    )
    room_count = rooms.count()
    return render(request, 'base/home.html',
                  {'rooms': rooms,
                   'topics': topics,
                   'room_count': room_count,
                   'room_messages': room_messages,
                   'total':total
                   })


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)

        return redirect('room', pk=room.id)
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i
    return render(request, 'base/room.html', {'room': room, 'room_messages': room_messages, 'participants': participants})


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect("home")
    return render(request, 'base/room_form.html', {'form': form})


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, 'base/room_form.html', {'form': form})


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect("home")

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect("home")

    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    total=Room.objects.filter()

    topics = Topic.objects.all()
    return render(request, 'base/profile.html',
                  {
                      'user': user,
                      'rooms': rooms,
                      'room_messages': room_messages,
                      'topics': topics,
                      'total':total
                  })

@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method=='POST':
        form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request, 'base/update-user.html',{'form':form})
