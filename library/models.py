from django.db import models
from django.conf import settings
from datetime import datetime
USER = settings.AUTH_USER_MODEL
from django.utils import timezone
now = timezone.now()



# LIBRARY
class Library(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=80)

    def __str__(self):
        return self.name
# BOOKS


class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    editor = models.CharField(max_length=80)
    jacket = models.ImageField(upload_to='images', default=None)  # image
    collection = models.CharField(max_length=80)
    genre = models.CharField(max_length=80)
    duration_max = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Title : ' + self.title + ' | Authors : ' + self.author +' | Library : ' + self.library.name


class Book_User(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compare_date(self):
        if(self.returned_at < now):
            return True
# FORUM


class Salon(models.Model):
    title = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# SESSION (Seance)


class Group(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class User_Group(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    isActive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
