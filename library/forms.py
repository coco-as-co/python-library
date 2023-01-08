from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Library

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LibraryForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    city = forms.CharField(max_length=80)
    address = forms.CharField(max_length=80)

    class Meta:
        model = Library
        fields = ['name', 'city', 'address']