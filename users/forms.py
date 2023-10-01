from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.ChoiceField(choices=[('','')] + [(i,i) for i in range(7,19)], initial='')
    confim_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'role', 'password', 'age',) 
        
    error_messages = {
        'invalid_username': (
            "Такой пользователь уже существует"
        ),
        
    }
    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise forms.ValidationError('Пароль слишком короткий')
        return password
    
    
    
    def clean_confim_password(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('confim_password'):
            raise forms.ValidationError('Пароли не совпадают')
        return cd.get('confim_password')
        
        
class MyAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Неверное имя или пароль"
        ),
        'inactive': ("This account is inactive."),
    }