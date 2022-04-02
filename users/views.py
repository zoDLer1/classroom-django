from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from main.models import Role
from .forms import RegisterForm
# Create your views here.



class Register(View):
    def get(self, request):
        roles = Role.objects.all()
        form = RegisterForm()
        return render(request, 'main/register.html', context={'roles': roles,'form':form, 'age_range': range(7,19)})


