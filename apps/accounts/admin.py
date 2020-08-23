from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BuiltInUserAdmin

from .models import User


# Register your models here.

@admin.register(User)
class UserAdmin(BuiltInUserAdmin):
    pass
