from django import forms
from .models import Student

class StudentSignupForm(forms.ModelForm):
    CLASS_CHOICES = [
        ('10', 'Class 10'),
        ('9', 'Class 9'),
        ('8', 'Class 8'),
    ]
    
    student_class = forms.ChoiceField(choices=CLASS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Student
        fields = ['name', 'student_class', 'interests', 'goals']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'interests': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Science, Arts, Technology, Sports'}),
            'goals': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Engineer, Doctor, Entrepreneur'}),
        }