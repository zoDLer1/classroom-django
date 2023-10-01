from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password
from main.models import Role
from classes.models import Class, Member
from tests.models import Test




class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password, role_id, age, firstname, lastname, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, role_id=role_id, age=age,first_name=firstname, last_name=lastname, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

        
    def create_user(self, username, email=None, password=None, role_id=None, age=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, role_id, age, **extra_fields)

    def create_superuser(self, username, role_id=None, email=None, password=None,age=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, role_id, age, **extra_fields)

class User(AbstractUser):   
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    avatar_url = models.CharField(max_length=150, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    age = models.IntegerField()
    
    objects = MyUserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role', 'age']
    def Classes(self):
        return Class.objects.filter(creator__id=self.id)
    def Tests(self):
        return Test.objects.filter(creator__id=self.id)
    def Members(self):
        return Member.objects.filter(user__id=self.id)