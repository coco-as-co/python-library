from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from .forms import SignUpForm , BookForm , Book , Library, LibraryForm, Book_User
from .models import Library
from datetime import datetime
from datetime import timedelta

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

        context = {'form': form, 'name': library.name}
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

def book(request):
    if request.user.is_authenticated :
        libraryList = Library.objects.filter(owner=request.user.id)
        if(len(libraryList) == 0):
             books = []
        else:
            books = []
            for lib in libraryList:
                books.extend(Book.objects.filter(library = lib.id))
        
        book_user = Book_User.objects.all().prefetch_related('book__book_user_set')
        return render(request, 'book/book.html', {'books': books, 'libraryList': libraryList, 'book_user': book_user})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def addBook(request):
    if request.user.is_authenticated:
            if request.method == 'POST':
                
                form = BookForm( request.POST,request.FILES,userId = request.user.id  )
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Book added successfully')

                    return redirect('book')
            else:
                form = BookForm(userId = request.user.id)
            
            context = {'form': form}
            return render(request, 'book/addBook.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def editBook(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        if request.method == 'POST':
            form = BookForm(request.POST,request.FILES,instance=book,userId = request.user.id)
            if form.is_valid():
                form.save()
                messages.success(request, 'Book updated successfully')

                return redirect('book')
        else:
            form = BookForm(instance=book,userId = request.user.id)
        
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

def bookList(request):
    if request.user.is_authenticated:
        libraryList = Library.objects.exclude(owner=request.user)
        print(libraryList)
        books = []
        if(libraryList.count() == 1):
            books = Book.objects.filter(library__in = libraryList)
        else:
            for lib in libraryList:
                books.extend(Book.objects.filter(library = lib.id))
        book_user = Book_User.objects.all().prefetch_related('book_user_set')
        return render(request, 'book/bookList.html', {'books': books, 'book_users': book_user})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def borrowBook(request, id):
    if request.user.is_authenticated:
        book_user = Book_User()
        book = Book.objects.get(id=id)
        book_user.book = book
        book_user.user = request.user
        book_user.borrowed_at = datetime.now()
        print(book.duration_max)
        book_user.returned_at = datetime.now() +  timedelta(days = book.duration_max)
        book_user.save()
        messages.success(request, 'Book borrowed successfully')

        return redirect('bookList')
    return HttpResponseNotFound('<h1>Page not found</h1>')