from django.shortcuts import render
from django.shortcuts import redirect
from chatservice.models import *
from chatservice.forms import UserForm, ChatroomForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


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
def chatrooms(request):
    user = request.user
    user_rooms = request.user.chatroom_set.all()
    all_rooms = Chatroom.objects.all()
    return render(request, "chatrooms.html", {'user': user, 'user_rooms': user_rooms, 'all_rooms': all_rooms})

@login_required
def chat(request, room_id):
    user = request.user
    chatroom = Chatroom.objects.get(id=room_id)
    chatroom_users = chatroom.users.all()
    chatroom_messages = chatroom.chatmessage_set.all()
    alert = None
    if (user not in chatroom_users):
        chatroom.users.add(user)
        chatroom.save()
        chatroom_users = chatroom.users.all()
        alert = "Joined chat room " + chatroom.name + "!"
    return render(request, "chat.html", {'user': user,
        'chatroom': chatroom, 'chatroom_users': chatroom_users,
        'chatroom_messages': chatroom_messages, 'alert': alert})

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
