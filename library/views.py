from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


def index(request):
    return HttpResponse("Hello, world. You're at the library index.")

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)