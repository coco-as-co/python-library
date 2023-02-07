from django.urls import path


from . import views


urlpatterns = [
    path('', views.libraries, name='libraries'),
    path('home/', views.home, name='home'),
    path('library/add/', views.add_library, name='add_library'),
    path('library/<int:library_id>/', views.detail_library, name='detail_library'),
    path('library/edit/<int:library_id>/', views.edit_library, name='edit_library'),
    path('library/delete/<int:library_id>/', views.delete_library, name='delete_library'),
    path('library/<int:library_id>/books/add/', views.add_book_library, name='add_book_library'),
    path('books/', views.bookList, name='bookList'),
    path('books/borrow/<int:id>', views.borrowBook, name='borrowBook'),
    path('books/return/<int:id>', views.returnBook, name='returnBook'),
    path('book/', views.book, name='book'),
    path('book/add', views.addBook, name='addBook'),
    path('book/edit/<int:id>', views.editBook, name='editBook'),
    path('book/delete/<int:id>', views.deleteBook, name='deleteBook'),
    path('profile', views.profile, name='profile'),
    path('profile/edit/<int:id>', views.editProfile, name='editProfile'),
    path('group/', views.groups, name='groups'),
    path('group/add/', views.add_group, name='add_group'),
    path('group/<int:group_id>/', views.detail_group, name='detail_group'),
    path('group/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('group/delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('group/<int:group_id>/sessions/add/', views.add_session, name='add_session'),
    path('group/<int:group_id>/sessions/edit/<int:session_id>/', views.edit_session, name='edit_session'),
    path('group/<int:group_id>/sessions/delete/<int:session_id>/', views.delete_session, name='delete_session'),
]

