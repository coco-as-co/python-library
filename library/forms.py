from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Library

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Pseudo",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pseudo'}))
    password = forms.CharField(label="Mot de passe", 
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Mot de passe'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
    email = forms.EmailField(max_length=254, required=True, label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=False, label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))
    last_name = forms.CharField(max_length=30, required=False, label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
    password1 = forms.CharField(max_length=30, required=True, label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(max_length=30, required=True, label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LibraryForm(forms.ModelForm):
    name = forms.CharField(max_length=80, required=True, label='Nom de la bibliothèque', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la bibliothèque'}))
    city = forms.CharField(max_length=80, required=True, label='Ville',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}))
    address = forms.CharField(max_length=80, required=True, label='Adresse',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}))

    class Meta:
        model = Library
        fields = ['name', 'city', 'address']