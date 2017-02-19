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
    name = forms.CharField(widget = forms.TextInput(attrs={'style':
        'width:300px'}))

    class Meta:
        model = Chatroom # We want to use Chatroom model ...
        # ... and the form should have the following fields
        fields = ('name',)

class ChatMessageForm(forms.ModelForm):
    message = forms.CharField(widget = forms.Textarea(attrs={'rows':
        2, 'cols': 80}))

    class Meta:
        model = ChatMessage # We want to use ChatMessage model ...
        # ... and the form should have the following fields
        fields = ('message',)

class EditUsernameForm(forms.ModelForm):

    class Meta:
        model = User # We want to use User model ...
        # ... and the form should have the following fields
        fields = ('username',)#('username', 'email', 'password')
