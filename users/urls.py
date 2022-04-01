from django.urls import path, include
from django.contrib.auth.forms import AuthenticationForm

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]

