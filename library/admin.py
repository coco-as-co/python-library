from django.contrib import admin

from .models import Library
from .models import Book
from .models import Book_User
from .models import Salon
from .models import Message
from .models import Group
from .models import User_Group
from .models import Session


admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Book_User)
admin.site.register(Salon)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(User_Group)
admin.site.register(Session)
