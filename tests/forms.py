from django import forms
from .models import Test, Question, Answer

class TestCreationForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":20}), required=False)
    class Meta:
        model = Test
        fields= ('name', 'description', 'creator')
        
class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields= ('name', 'test')
        
class AnswerCreationForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields= ('value', 'question', 'right')