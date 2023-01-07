from django.urls import path


from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('addBook/', views.addBook, name='addBook'),
    path('editBook/<int:id>', views.editBook, name='editBook'),
    path('deleteBook/<int:id>', views.deleteBook, name='deleteBook'),
]

