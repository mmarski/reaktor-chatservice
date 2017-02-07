from django.shortcuts import render
from django.shortcuts import redirect
from projekti.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html", {})

def chatrooms(request):
    pass

def chat(request):
    pass
