from django.shortcuts import render
from main.models import Role
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    return render(request,'main/index.html')

