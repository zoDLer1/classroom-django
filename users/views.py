from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic import View
from .forms import RegisterForm, MyAuthForm
from .models import User
from django.contrib.auth import authenticate, login
# Create your views here.


        
class MyLoginView(LoginView):
    authentication_form = MyAuthForm
    template_name = "users/login.html"
        
class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', context={'form': form})
    
    def post(self, request):
        print(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            role_id = form.cleaned_data.get('role').id
            age = form.cleaned_data.get('age')
            
            
            User.objects.create_user(username=username, password=password, email=email, role_id=role_id, age=age, firstname=firstname, lastname=lastname)
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        print(form.errors)
        return render(request, 'users/register.html', context={'form':form})