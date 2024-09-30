from django import forms
from django.contrib.auth.models import User
from . import models
from .models import IssuedBook

class IssueBookForm(forms.ModelForm):
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name [ISBN]", to_field_name="isbn", label="Book (Name and ISBN)")
    name2 = forms.ModelChoiceField(queryset=models.Student.objects.all(), empty_label="Name [Branch] [Class] [Roll No]", to_field_name="user", label="Student Details")
    class Meta:
        model=IssuedBook
        fields=['isbn2','name2']
        
    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})
