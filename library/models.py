from django.db import models

# LIBRARY


class Library(models.Model):
    # owner = models.ForeignKey(User)
    name = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=80)


# BOOKS


class Genre(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Collection(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    editor = models.CharField(max_length=80)
    jacket = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# FORUM


class Salon(models.Model):
    title = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    # user = models.ForeignKey(User)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# SESSION (Seance)


class Group(models.Model):
    # owner = models.ForeignKey(User)
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Group(models.Model):
    # user = models.ForeignKey(User)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    isActive = models.BooleanField(max_length=80, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Group_Session(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
