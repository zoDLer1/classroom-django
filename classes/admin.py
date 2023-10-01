from django.contrib import admin
from django.contrib.admin import display
from .models import *
# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
        list_display = ('id', 'name', 'creator', 'created_at', 'type')
        
@admin.register(Member)      
class MemberAdmin(admin.ModelAdmin):
        list_display = ('id', 'get_classname', 'user')
        @display(description='class')
        def get_classname(self, obj):
                return obj.current_class.name
        

        
@admin.register(WaitingRoom)      
class WaitingRoomAdmin(admin.ModelAdmin):
        list_display = ('id', 'get_classname', 'user')
        @display(description='class')
        def get_classname(self, obj):
                return obj.current_class.name
        
@admin.register(InviteLink)
class InviteLinkAdmin(admin.ModelAdmin):
        list_display = ('id', 'code', 'current_class', 'created_at')

@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
        list_display = ('id', 'name')
