from django.urls import path


from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('book/add', views.addBook, name='addBook'),
    path('book/edit/<int:id>', views.editBook, name='editBook'),
    path('book/delete/<int:id>', views.deleteBook, name='deleteBook'),
]

