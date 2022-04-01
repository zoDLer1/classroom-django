from django.shortcuts import render
from main.models import Role
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    return render(request,'main/index.html')

def login(request):
    form = AuthenticationForm()
    return render(request, 'main/login.html', context={'form':form})

def register(request):
    roles = Role.objects.all()
    return render(request, 'main/register.html', context={'roles': roles, 'age_range': range(7,19)})