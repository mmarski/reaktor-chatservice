from django.shortcuts import render
from django.shortcuts import redirect
from chatservice.models import *
from chatservice.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.core import serializers
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return redirect('chatrooms')
    return render(request, "index.html", {})

def register(request):
    if request.user.is_authenticated:
        return redirect('chatrooms')
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request,
                "Account created successfully! Please log in.")
            return redirect('chatrooms')
        else:
            messages.error(request,
                "Invalid input. Your chosen username may be in use.")
            return redirect('register')
    else:
        user_form = UserForm()
    return render(request, "accounts/register.html", {'form': user_form,
        'active_tab': 'register'})

@login_required
def profile(request):
    if request.method == 'POST':
        name_edit_form = EditUsernameForm(data=request.POST,
            instance=request.user)
        if name_edit_form.is_valid():
            user = name_edit_form.save()
            user.save()
            messages.success(request, "Username changed successfully!")
        else:
            messages.error(request,
                "Could not modify username. You must choose a unique name.")
        return redirect('profile')
    else:
        name_edit_form = EditUsernameForm(instance=request.user)
    return render(request, "accounts/profile.html", {'user': request.user,
        'form': name_edit_form, 'active_tab': 'profile'})

@login_required
def chatrooms(request):
    user = request.user
    user_rooms = request.user.chatroom_set.all()
    all_rooms = Chatroom.objects.all()
    return render(request, "chatrooms.html", {'user': user,
        'user_rooms': user_rooms, 'all_rooms': all_rooms,
        'active_tab': 'chatrooms'})

@login_required
def chat(request, room_id):
    user = request.user
    chatroom = Chatroom.objects.get(id=room_id)
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST['message'])
            ChatMessage.objects.create(message=request.POST['message'],
                user=user, chatroom=chatroom)
            return redirect('chat', chatroom.id)
        elif request.method == 'GET':
            chatroom_messages = chatroom.chatmessage_set.all()
            serial = serializers.serialize('json', chatroom_messages, fields=(
                'message', 'user', 'created'))
            msgjson = json.dumps(serial)
            return HttpResponse(msgjson, content_type="application/json")
        return
    msg_form = ChatMessageForm()
    chatroom_users = chatroom.users.all()
    chatroom_messages = chatroom.chatmessage_set.all()
    serial = serializers.serialize('json', chatroom_messages, fields=(
        'message', 'user', 'created'))
    msgjson = json.dumps(serial)
    if (user not in chatroom_users):
        chatroom.users.add(user)
        chatroom.save()
        chatroom_users = chatroom.users.all()
        messages.success(request, "Joined chat room " + chatroom.name + "!")
    return render(request, "chat.html", {'user': user,
        'chatroom': chatroom, 'chatroom_users': chatroom_users,
        'chatroom_messages': msgjson, 'form': msg_form})

@login_required
def create_room(request):
    if request.method == 'POST':
        create_form = ChatroomForm(data=request.POST)
        if create_form.is_valid():
            chatroom = create_form.save()
            chatroom.save()
            return redirect('chat', chatroom.id)
    else:
        create_form = ChatroomForm()
    return render(request, "create_room.html", {'form': create_form})
