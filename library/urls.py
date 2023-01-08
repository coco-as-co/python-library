from django.urls import path

from . import views

urlpatterns = [
    path('', views.libraries, name='libraries'),
    path('home/', views.home, name='home'),
    path('library/add/', views.add_library, name='add_library'),
    path('library/<int:library_id>/', views.detail_library, name='detail_library'),
    path('library/edit/<int:library_id>/', views.edit_library, name='edit_library'),
    path('library/delete/<int:library_id>/', views.delete_library, name='delete_library'),
    #path('library/<int:library_id>/add/', views.add_book, name='add_book'),
]
