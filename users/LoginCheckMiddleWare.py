from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse, include
from django.http import HttpResponseRedirect, HttpResponse
import users
from users import urls


def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == "1":
            return redirect('users:admin_home')
        elif request.user.user_type == "2":
            return redirect('users:staff_home')
        elif request.user.user_type == "3":
            return redirect('users:developer_home')
        else:
            return redirect('users:user_home')
    else:
        return redirect("users:login")


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        #  Check whether the user is logged in or not
        allowed_urls = users.urls
        if user.is_authenticated:
            index(request)
        elif request.path.startswith(reverse('admin:index')) or request.path.startswith(reverse('users:index')):
            pass
            #return redirect(reverse("users:login"))
        else:
            pass
            #return HttpResponse('login first')




"""
if request.path in self.WHITELISTED_URLS:
            return None
        else:
            return HttpResponseRedirect(self.REDIRECT_URL)

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user
        #  Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "users.AdminView":
                    pass
                elif modulename == "users.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("users:admin_home")
            
            elif user.user_type == "2":
                if modulename == "users.StaffView":
                    pass
                elif modulename == "users.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("users:staff_home")
            
            elif user.user_type == "3":
                if modulename == "users.DevelopViews":
                    pass
                elif modulename == "users.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("users:developer_home")
            
            elif user.user_type == "4":
                if modulename == "users.UserViews":
                    pass
                elif modulename == "users.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("users:user_home")
            else:
                return redirect("users:login")

        else:
            pass
"""