from django.contrib import admin

# Register your models here.

from .models import User, UserFunds, Position

admin.site.register(User)
admin.site.register(UserFunds)
admin.site.register(Position)
