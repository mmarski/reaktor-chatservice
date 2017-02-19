from django.shortcuts import render
from django.shortcuts import redirect
from chatservice.models import *
from chatservice.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import json
from django.core import serializers
from django.http import HttpResponse


def index(request):
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
            return redirect('chatrooms')
    else:
        user_form = UserForm()
    return render(request, "accounts/register.html", {'form': user_form})

@login_required
def profile(request):
    return render(request, "accounts/profile.html", {})

@login_required
def chatrooms(request):
    user = request.user
    user_rooms = request.user.chatroom_set.all()
    all_rooms = Chatroom.objects.all()
    return render(request, "chatrooms.html", {'user': user,
        'user_rooms': user_rooms, 'all_rooms': all_rooms})

@login_required
def chat(request, room_id):
    user = request.user
    chatroom = Chatroom.objects.get(id=room_id)
    alert = None
    if request.is_ajax():
        print("ajax")
        if request.method == 'POST':
            print(request.POST['message'])
            m = ChatMessage.objects.create(message=request.POST['message'],
                user=user, chatroom=chatroom)
            print(str(m.created))
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
        alert = "Joined chat room " + chatroom.name + "!"
    return render(request, "chat.html", {'user': user,
        'chatroom': chatroom, 'chatroom_users': chatroom_users,
        'chatroom_messages': msgjson, 'alert': alert,
        'form': msg_form})

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
