from django.shortcuts import render
from users.models import CustomUser


def user_home(request):
    return render(request, 'users/user_template/index.html')


