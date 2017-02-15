from django.contrib.auth.models import User
from django import forms
from chatservice.models import Chatroom, ChatMessage

class UserForm(forms.ModelForm):
    # use password widget so password isn't shown
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User # We want to use User model ...
        # ... and the form should have the following fields
        fields = ('username', 'password')#('username', 'email', 'password')

class ChatroomForm(forms.ModelForm):

    class Meta:
        model = Chatroom # We want to use Chatroom model ...
        # ... and the form should have the following fields
        fields = ('name',)

class ChatMessageForm(forms.ModelForm):

    class Meta:
        model = ChatMessage # We want to use ChatMessage model ...
        # ... and the form should have the following fields
        fields = ('message',)
