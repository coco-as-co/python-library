from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from .forms import SignUpForm, LibraryForm
from .models import Library


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
        return render(request, './home.html')
    return HttpResponseNotFound('<h1>Page not found</h1>')

def libraries(request):
    if request.user.is_authenticated:
        libraries = Library.objects.all().exclude(owner=request.user)
        myLibraries = Library.objects.filter(owner=request.user)

        context = {'libraries': libraries, 'myLibraries': myLibraries}

        return render(request, 'library/index.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def add_library(request):
    if request.user.is_authenticated == False:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, 'Library created successfully')

            return redirect('libraries')
    else:
        form = LibraryForm()

    context = {'form': form}
    return render(request, 'library/add.html', context)

def detail_library(request, library_id):
    if request.user.is_authenticated:
        library = Library.objects.get(id=library_id)
        context = {'library': library}
        return render(request, 'library/detail.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def edit_library(request, library_id):
    if request.user.is_authenticated:
        library = Library.objects.get(id=library_id)

        if library.owner != request.user:
            return redirect('libraries')

        if request.method == 'POST':
            form = LibraryForm(request.POST, instance=library)
            if form.is_valid():
                form.save()
                messages.success(request, 'Library updated successfully')

                return redirect('libraries')
        else:
            form = LibraryForm(instance=library)

        context = {'form': form}
        return render(request, 'library/edit.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def delete_library(request, library_id):
    if request.user.is_authenticated:
        library = Library.objects.get(id=library_id)

        if library.owner != request.user:
            return redirect('libraries')

        library.delete()
        messages.success(request, 'Library deleted successfully')

        return redirect('libraries')
    return HttpResponseNotFound('<h1>Page not found</h1>')