from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Role
# Create your models here.
class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    avatar_url = models.CharField(null=True, max_length=150)
    