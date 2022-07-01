from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class UserModel(UserAdmin):
    change_list_template = 'smuggler/change_list.html'


admin.site.register(CustomUser, UserModel)
