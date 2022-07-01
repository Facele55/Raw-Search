from django.shortcuts import render
from users.models import CustomUser
from core.models import *


def developer_home(request):
    context = {
    }
    return render(request, 'users/develop_template/index.html', context)

