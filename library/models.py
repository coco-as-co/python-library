from django.db import models
from django.conf import settings

USER = settings.AUTH_USER_MODEL


# LIBRARY


class Library(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=80)


# BOOKS


class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    editor = models.CharField(max_length=80)
    jacket = models.CharField(max_length=80)  # image
    collection = models.CharField(max_length=80)
    genre = models.CharField(max_length=80)
    duration_max = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book_User(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# FORUM


class Salon(models.Model):
    title = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class User_Group(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
