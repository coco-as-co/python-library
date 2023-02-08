from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from .models import Book, Book_User, Library, Session, Group, Message
import datetime

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Pseudo",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Pseudo"}
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label="Prénom",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Prénom"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label="Nom",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom"}),
    )
    password1 = forms.CharField(
        max_length=30,
        required=True,
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        ),
    )
    password2 = forms.CharField(
        max_length=30,
        required=True,
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirmation du mot de passe",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=False, label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))
    last_name = forms.CharField(max_length=30, required=False, label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))

    class Meta:
        model = User
        fields = [ 'email', 'first_name', 'last_name']

# class LibrarySelect(forms.Select):
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super().create_option(name, value, label, selected, index, subindex, attrs)
#         return option


class BookForm(forms.ModelForm):
    title = forms.CharField(
        max_length=250,
        required=True,
        label="Titre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre"}),
    )
    author = forms.CharField(
        max_length=80,
        required=True,
        label="Auteur",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Auteur"}
        ),
    )
    library = forms.ModelChoiceField(
        queryset=Library.objects.all(),
        label="Bibliothèque",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    editor = forms.CharField(
        max_length=80,
        required=True,
        label="Editeur",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Editeur"}
        ),
    )
    collection = forms.CharField(
        max_length=80,
        required=True,
        label="Collection",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Collection"}
        ),
    )
    genre = forms.CharField(
        max_length=80,
        required=True,
        label="Genre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Genre"}),
    )
    duration_max = forms.IntegerField(
        max_value=730,
        min_value=1,
        required=True,
        label="Durée max en jours",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Durée max", "value": 1, "min": 1}
        ),
    )
    jacket = forms.ImageField(
        required=False,
        label="Jaquette",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user =  kwargs.pop('user_id',None)
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['library'].queryset = Library.objects.filter(owner=user)
    
class BookLibraryForm(forms.ModelForm):
    title = forms.CharField(max_length=250, required=True, label='Titre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}))
    author = forms.CharField(max_length=80, required=True, label='Auteur',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auteur'}))
    library = forms.ModelChoiceField(queryset=Library.objects.all(), label='Bibliothèque',
        widget=forms.Select(attrs={'class': 'form-control'}))
    editor = forms.CharField(max_length=80, required=True, label='Editeur',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Editeur'}))
    collection = forms.CharField(max_length=80, required=True, label='Collection',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Collection'}))
    genre = forms.CharField(max_length=80, required=True, label='Genre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genre'}))
    duration_max = forms.CharField(max_length=80,required=True, label='Durée max en jours',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Durée max', 'type': 'number'}))
    jacket = forms.FileField(required=False, label='Jaquette',
        widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        library = kwargs.pop('lib_id',None)
        super(BookLibraryForm, self).__init__(*args, **kwargs)
        self.fields['library'].queryset = Library.objects.filter(id=library)
        self.fields['library'].widget.attrs['disabled'] = True
        self.fields['library'].initial = library
        self.fields['library'].required = False


class LibraryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=80,
        required=True,
        label="Nom de la bibliothèque",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nom de la bibliothèque"}
        ),
    )
    city = forms.CharField(
        max_length=80,
        required=True,
        label="Ville",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ville"}),
    )
    address = forms.CharField(
        max_length=80,
        required=True,
        label="Adresse",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Adresse"}
        ),
    )

    class Meta:
        model = Library
        fields = ['name', 'city', 'address']

class GroupForm(forms.ModelForm):
    name = forms.CharField(max_length=80, required=True, label='Nom du groupe', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du groupe'}))

    class Meta:
        model = Group
        fields = ['name']

class SessionForm(forms.ModelForm):
    date = forms.DateField(required=True, label='Date',
        widget=AdminDateWidget(attrs={'class': 'form-control', 'type': 'date', 'min': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), 'placeholder': 'Date'}))
    hour = forms.TimeField(required=True, label='Heure',
        widget=AdminTimeWidget(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Heure'}))
    
    class Meta:
        model = Session
        fields = ['date', 'hour']
        widgets = {
            "date": AdminDateWidget,
            "hour": AdminTimeWidget
        }

class SalonForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        label="Message",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )

    class Meta:
        model = Message
        fields = ["content"]
