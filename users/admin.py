from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
        list_display = ('id', 'username', 'email','role', 'first_name', 'last_name', 'is_staff')