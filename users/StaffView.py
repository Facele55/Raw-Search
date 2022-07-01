from django.shortcuts import render


def staff_home(request):
    return render(request, 'users/staff_template/index.html')


