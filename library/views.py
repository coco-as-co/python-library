from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q

from django.contrib import messages
from .forms import SignUpForm , BookForm, LibraryForm, Book_User , BookLibraryForm , ProfileForm, GroupForm, SessionForm, SalonForm, User
from .models import Library, Session, User_Group, Salon, Message, Group, Book, Book_User
from datetime import datetime, timedelta

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
        my_libraries = Library.objects.filter(owner=request.user)

        context = {'libraries': libraries, 'myLibraries': my_libraries}

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
            form = BookLibraryForm(request.POST, request.FILES, lib_id = library_id)
            if form.is_valid():
                form.instance.library = library
                form.save()
                messages.success(request, 'Book added successfully')

                return redirect('detail_library', library_id)
        else:
            form = BookLibraryForm(lib_id = library_id)
            form.instance.library = library

        context = {'form': form, 'library': library}
        return render(request, 'library/books/add.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def book(request):
    if request.user.is_authenticated :
        library_list = Library.objects.filter(owner=request.user.id)
        if(len(library_list) == 0):
            books = []
        else:
            books = []
            for lib in library_list:
                books.extend(Book.objects.filter(library = lib.id))
        
        book_user = Book_User.objects.all().prefetch_related('book__book_user_set')
        return render(request, 'book/book.html', {'books': books, 'library_list': library_list, 'book_user': book_user})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def add_book(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            
            form = BookForm( request.POST,request.FILES,user_id = request.user.id  )
            if form.is_valid() and form.instance.duration_max > 0:
                form.save()
                messages.success(request, 'Book added successfully')

                return redirect('book')
        else:
            form = BookForm(user_id = request.user.id)
        
        context = {'form': form}
        return render(request, 'book/add.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def edit_book(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)

        if book.library.owner == request.user:
            if request.method == 'POST':
                form = BookForm(request.POST,request.FILES,instance=book,user_id = request.user.id)
                if form.is_valid() and form.instance.duration_max > 0:
                    form.save()
                    messages.success(request, 'Book updated successfully')

                    return redirect('book')
            else:
                form = BookForm(instance=book,user_id = request.user.id)
            
            context = {'form': form}
            return render(request, 'book/edit.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def delete_book(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        if book.library.owner == request.user:
            book.delete()
            messages.success(request, 'Book deleted successfully')

            return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseNotFound('<h1>Page not found</h1>')

def book_list(request):
    if request.user.is_authenticated:
        library_list = Library.objects.exclude(owner=request.user)
        books = []
        if(library_list.count() == 1):
            books = Book.objects.filter(library__in = library_list)
        else:
            for lib in library_list:
                books.extend(Book.objects.filter(library = lib.id))

        keyword = request.GET.get('search')
        if keyword:
          keyword = keyword.strip()
          books = books.filter(
            Q(title__icontains=keyword) |
            Q(author__icontains=keyword) |
            Q(editor__icontains=keyword) |
            Q(collection__icontains=keyword) |
            Q(genre__icontains=keyword) |
            Q(library__address__icontains=keyword) |
            Q(library__city__icontains=keyword) |
            Q(library__name__icontains=keyword)
          ).distinct()

        book_user = Book_User.objects.all().prefetch_related('book_user_set')
        return render(request, 'book/list.html', {'books': books, 'book_users': book_user})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def borrow_book(request, id):
    if request.user.is_authenticated:
        book_user = Book_User()
        book = Book.objects.get(id=id)
        book_user.book = book
        book_user.user = request.user
        book_user.borrowed_at = datetime.now()
        book_user.returned_at = datetime.now() +  timedelta(days = book.duration_max)
        book_user.save()
        messages.success(request, 'Book borrowed successfully')

        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseNotFound('<h1>Page not found</h1>')

def return_book(request, id):
    if request.user.is_authenticated:
        book_user = Book_User.objects.get(book=id)
        book_user.delete()
        messages.success(request, 'Book returned successfully')

        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseNotFound('<h1>Page not found</h1>')

def profile(request):
    if request.user.is_authenticated:
        # user = User.objects.get(id=request.user.id)
        user = request.user
        books = Book_User.objects.filter(user = request.user.id).exclude(returned_at__lt=datetime.now())
        books_late = Book_User.objects.filter(user = request.user.id).exclude(returned_at__gt=datetime.now())
        return render(request, 'profile/index.html', {'user': user, 'books': books, 'books_late': books_late})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def edit_profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
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
        sessions = None

        exists = User_Group.objects.filter(user = request.user.id, group = group_id).exists()
        is_owner = group.owner == request.user

        print(exists)
        print(is_owner)

        if exists or is_owner:
            sessions = Session.objects.filter(group = group_id)

            context = {'group': group, 'sessions': sessions}
            return render(request, 'group/detail.html', context)
        
        return redirect('groups')

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

def join_group(request, group_id):
    if request.user.is_authenticated:
        group = Group.objects.get(id=group_id)
        user_group = User_Group()
        user_group.user = request.user
        user_group.group = group
        user_group.save()
        messages.success(request, 'Group joined successfully')

        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseNotFound('<h1>Page not found</h1>')

def leave_group(request, group_id):
    if request.user.is_authenticated:
        group = Group.objects.get(id=group_id)
        user_group = User_Group.objects.filter(user = request.user.id, group = group_id).first()
        user_group.delete()
        messages.success(request, 'Group left successfully')

        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseNotFound('<h1>Page not found</h1>')

def add_session(request, group_id):
    if request.user.is_authenticated:
        group = Group.objects.filter(owner = request.user.id, id = group_id).first()

        if group:
            if request.method == 'POST':
                form = SessionForm(request.POST)
                if form.is_valid():
                    if form.instance.date >= datetime.date(datetime.now() + timedelta(days=1)):
                        form.instance.group = group
                        form.save()
                        messages.success(request, 'Session added successfully')

                        return redirect('detail_group', group_id)
            else:
                form = SessionForm()
            
            context = {'form': form}
            return render(request, 'group/session/add.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def edit_session(request, group_id, session_id):
    if request.user.is_authenticated:
        is_owner = Group.objects.filter(owner = request.user.id, id = group_id).exists()

        if is_owner:
            session = Session.objects.get(id=session_id)
            if request.method == 'POST':
                form = SessionForm(request.POST,instance=session)
                if form.is_valid():
                    if form.instance.date >= datetime.date(datetime.now() + timedelta(days=1)):
                        form.save()
                        messages.success(request, 'Session updated successfully')

                        return redirect('detail_group', group_id)
            else:
                form = SessionForm(instance=session)
            
            context = {'form': form, 'session': session}
            return render(request, 'group/session/edit.html',context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def delete_session(request, group_id, session_id):
    if request.user.is_authenticated:
        is_owner = Group.objects.filter(owner = request.user.id, id = group_id).exists()

        if is_owner:
            session = Session.objects.get(id=session_id)
            session.delete()
            messages.success(request, 'Session deleted successfully')

        return redirect('detail_group', group_id)
    return HttpResponseNotFound('<h1>Page not found</h1>')
def salons(request):
    if request.user.is_authenticated:
        salons = Salon.objects.all()
        messages = Message.objects.filter(salon__in=salons)
        for salon in salons:
            salon.messages = messages.filter(salon=salon.id)
            
        context = {'salons': salons, 'messages': messages}
        return render(request, 'salon/index.html', context)
    return HttpResponseNotFound('<h1>Page not found</h1>')

def detail_salon(request, salon_id):
    if request.user.is_authenticated == False:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    salon = Salon.objects.get(id=salon_id)

    messages = Message.objects.filter(salon=salon_id)
    paginator = Paginator(messages, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.salon = salon
            form.save()

            # Return to the last page
            messages = Message.objects.filter(salon=salon_id)
            paginator = Paginator(messages, 5)
            page_number = paginator.num_pages
            page_obj = paginator.get_page(page_number)
    else:
        form = SalonForm()

    context = {'form': form, 'salon': salon, 'messages': messages, 'page_obj': page_obj}
    return render(request, 'salon/salon.html', context)
