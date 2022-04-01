from django import forms
from users.models import User

class AuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('username', 'password', ) 