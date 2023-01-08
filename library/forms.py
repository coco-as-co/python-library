from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book
from .models import Library




class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


# class LibrarySelect(forms.Select):
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super().create_option(name, value, label, selected, index, subindex, attrs)
#         return option

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user =  kwargs.pop('userId',None)
        super(BookForm, self).__init__(*args, **kwargs)
        print(user)

        self.fields['library'].queryset = Library.objects.filter(owner=user)
    
        
   

class LibraryForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    city = forms.CharField(max_length=80)
    address = forms.CharField(max_length=80)

    class Meta:
        model = Library
        fields = ['name', 'city', 'address']