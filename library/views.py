from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from .forms import SignUpForm , BookForm , Book , Library, LibraryForm, Book_User , BookLibraryForm , ProfileForm, User, GroupForm, Group, SessionForm
from .models import Library
from datetime import datetime
from datetime import timedelta

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing_page.html')

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
        books = Book.objects.filter(library=library_id)
        context = {'library': library, 'books': books}
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

def add_book_library(request, library_id):
    if request.user.is_authenticated:
        library = Library.objects.get(id=library_id)

        if library.owner != request.user:
            return redirect('libraries')

        if request.method == 'POST':
            form = BookLibraryForm(request.POST, request.FILES, libraryId = library.id)
            print(form.errors)
            if form.is_valid():
                form.instance.library = library
                form.save()
                messages.success(request, 'Book added successfully')

                return redirect('detail_library', library_id=library_id)
        else:
            form = BookLibraryForm(libraryId = library.id)
            form.instance.library = library

        context = {'form': form, 'library': library}
        return render(request, 'library/books/add.html', context)
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


def returnBook(request, id):
    if request.user.is_authenticated:
        book_user = Book_User.objects.get(book=id)
        book_user.delete()
        messages.success(request, 'Book returned successfully')

        return redirect('book')
    return HttpResponseNotFound('<h1>Page not found</h1>')

def profile(request):
    if request.user.is_authenticated:
        # user = User.objects.get(id=request.user.id)
        user = request.user
        books = Book_User.objects.filter(user = request.user.id).exclude(returned_at__lt=datetime.now())
        books_late = Book_User.objects.filter(user = request.user.id).exclude(returned_at__gt=datetime.now())
        return render(request, 'profile/index.html', {'user': user, 'books': books, 'books_late': books_late})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def editProfile(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        if request.method == 'POST':
            form = ProfileForm(request.POST,instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'profile updated successfully')

                return redirect('profile')
        else:
            form = form = ProfileForm(instance=user)
        
        context = {'form': form}
        return render(request, 'profile/edit.html',context)
def groups(request):
    if request.user.is_authenticated:
        groups = Group.objects.all().exclude(owner=request.user)
        myGroups = Group.objects.filter(owner=request.user)

        context = {'groups': groups, 'myGroups': myGroups}

        return render(request, 'group/index.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def add_group(request):
    if request.user.is_authenticated == False:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, 'Group created successfully')

            return redirect('detail_group', form.instance.id)
    else:
        form = GroupForm()

    context = {'form': form}
    return render(request, 'group/add.html', context)

def detail_group(request, group_id):
    if request.user.is_authenticated:
        group = Group.objects.get(id=group_id)
        context = {'group': group}
        return render(request, 'group/detail.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def edit_group(request, group_id):
    if request.user.is_authenticated:
        group = Group.objects.get(id=group_id)

        if group.owner != request.user:
            return redirect('groups')

        if request.method == 'POST':
            form = GroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                messages.success(request, 'Group updated successfully')

                return redirect('detail_group', group_id=group_id)
        else:
            form = GroupForm(instance=group)

        context = {'form': form, 'name': group.name}
        return render(request, 'group/edit.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def delete_group(request, group_id):
    if request.user.is_authenticated:
        group = Group.objects.get(id=group_id)

        if group.owner != request.user:
            return redirect('groups')

        group.delete()
        messages.success(request, 'Group deleted successfully')

        return redirect('groups')
    return HttpResponseNotFound('<h1>Page not found</h1>')

def sessions(request, group_id):
    if request.user.is_authenticated:
        exists = User_Group.objects.filter(user = request.user.id, group = group_id).exists()

        if exists:
            sessions = Session.objects.filter(group = group_id)
            return render(request, 'profile/sessions.html', {'sessions': sessions})

    return HttpResponseNotFound('<h1>Page not found</h1>')

def detail_session(request, id):
    if request.user.is_authenticated:
        session = Session.objects.get(id=id)
        exist = User_Group.objects.filter(user = request.user.id, group = session.group.id).exists()

        if exist:
            return render(request, 'profile/detail_session.html', {'session': session})

    return HttpResponseNotFound('<h1>Page not found</h1>')

def add_session(request, group_id):
    if request.user.is_authenticated:
        is_owner = Group.objects.filter(owner = request.user.id, id = group_id).exists()

        if is_owner:
            if request.method == 'POST':
                form = SessionForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Session added successfully')

                    return redirect('sessions')
            else:
                form = SessionForm()
            
            context = {'form': form}
            return render(request, 'profile/add_session.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def edit_session(request, group_id, session_id):
    if request.user.is_authenticated:
        is_owner = Group.objects.filter(owner = request.user.id, id = group_id).exists()

        if is_owner:
            session = Session.objects.get(id=session_id)
            if request.method == 'POST':
                form = SessionForm(request.POST,instance=session)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Session updated successfully')

                    return redirect('sessions')
            else:
                form = SessionForm(instance=session)
            
            context = {'form': form}
            return render(request, 'profile/edit_session.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def delete_session(request, group_id, session_id):
    if request.user.is_authenticated:
        is_owner = Group.objects.filter(owner = request.user.id, id = group_id).exists()

        if is_owner:
            session = Session.objects.get(id=session_id)
            session.delete()
            messages.success(request, 'Session deleted successfully')

            return redirect('sessions')
    return HttpResponseNotFound('<h1>Page not found</h1>')
