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
    path('books/', views.book_list, name='book_list'),
    path('books/borrow/<int:id>', views.borrow_book, name='borrow_book'),
    path('books/return/<int:id>', views.return_book, name='return_book'),
    path('book/', views.book, name='book'),
    path('book/add', views.add_book, name='add_book'),
    path('book/edit/<int:id>', views.edit_book, name='edit_book'),
    path('book/delete/<int:id>', views.delete_book, name='delete_book'),
    path('profile', views.profile, name='profile'),
    path('profile/edit/<int:id>', views.edit_profile, name='edit_profile'),
    path('group/', views.groups, name='groups'),
    path('group/add/', views.add_group, name='add_group'),
    path('group/<int:group_id>/', views.detail_group, name='detail_group'),
    path('group/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('group/delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('group/<int:group_id>/sessions/add/', views.add_session, name='add_session'),
    path('group/<int:group_id>/sessions/edit/<int:session_id>/', views.edit_session, name='edit_session'),
    path('group/<int:group_id>/sessions/delete/<int:session_id>/', views.delete_session, name='delete_session'),
]

