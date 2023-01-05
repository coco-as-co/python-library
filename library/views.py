from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from .forms import SignUpForm


def index(request):
    return HttpResponse("Hello, world. You're at the library index.")

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')

            return redirect('login')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def home(request):
    if request.user.is_authenticated:
        return render(request, 'library/home.html')
    return HttpResponseNotFound('<h1>Page not found</h1>')