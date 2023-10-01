from django import forms
from .models import Class, ClassType

class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields= ('name', 'creator')
        
class TypeToggle(forms.ModelForm):
    class Meta:
        model = Class
        fields= ('type', 'name', )
        widgets = {
            'name': forms.TextInput(attrs={'class':'form__input', "v-if":"edit"}),
            'type': forms.Select(attrs={'class':'form__input',"v-if":"edit"})
        }

    
    
    
    