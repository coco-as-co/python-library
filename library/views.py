from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from .forms import SignUpForm , AddBookForm , Book


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

def book(request):
    if request.user.is_authenticated:
        books = Book.objects.all()
        return render(request, 'book/book.html', {'books': books})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def addBook(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddBookForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Book added successfully')

                return redirect('book')
        else:
             form = AddBookForm()
        
        context = {'form': form}
        return render(request, 'book/addBook.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def editBook(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        if request.method == 'POST':
            form = AddBookForm(request.POST,request.FILES,instance=book)
            if form.is_valid():
                form.save()
                messages.success(request, 'Book updated successfully')

                return redirect('book')
        else:
            form = AddBookForm(instance=book)
        
        context = {'form': form}
        return render(request, 'book/editBook.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def deleteBook(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, 'Book deleted successfully')

        return redirect('book')
    return HttpResponseNotFound('<h1>Page not found</h1>')

