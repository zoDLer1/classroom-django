from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
        list_display = ('id', 'name', 'description', 'creator')
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
        list_display = ('id', 'name', 'test')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
        list_display = ('id', 'value', 'question', 'right')
        
@admin.register(TestForClass)
class TestForClassAdmin(admin.ModelAdmin):
        list_display = ('id', 'current_class', 'test', 'created_at')
        
@admin.register(PassedTest)
class PassedTestAdmin(admin.ModelAdmin):
        list_display = ('id', 'user', 'test_for_class')
        
@admin.register(PassedQuestion)
class PassedQuestionAdmin(admin.ModelAdmin):
        list_display = ('id', 'question', 'answer', 'passed_test')