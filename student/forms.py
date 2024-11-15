from django.forms import forms

from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'ph_no', 'branch', 'batch_code']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter student name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter student email'}),
            'ph_no': forms.NumberInput(attrs={'placeholder': 'Enter phone number'}),
            'branch': forms.TextInput(attrs={'placeholder': 'Enter branch'}),
            'batch_code': forms.TextInput(attrs={'placeholder': 'Enter batch code (e.g., A1)'}),
        }
