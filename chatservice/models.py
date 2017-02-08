from django.db import models
from django.contrib.auth.models import User

# Extra data model for a user, to store user nickname
class Extra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=20)

# Model to represent a single chatroom which contains users and messages
class Chatroom(models.Model):
    name = models.CharField(unique=True, max_length=255)
    users = models.ManyToManyField(User)

# Model to represent a single chat message from a user in a chatroom
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
