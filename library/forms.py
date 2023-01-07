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


class LibrarySelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        return option
class AddBookForm(forms.ModelForm):
    # library = Library.objects.all()
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {'library': LibrarySelect}
        # widgets = {
        #     'studio':forms.SelectMultiple(attrs={'class': 'form-control'})
        # }