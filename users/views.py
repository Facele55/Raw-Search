import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from users.EmailBackEnd import EmailBackEnd
from users.LoginCheckMiddleWare import *
from users.forms import LoginForm, SignUpForm
from users.models import *

logger = logging.getLogger("django")


@sensitive_post_parameters('password')
def login_page(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("users:index")
            else:
                messages.error(request, _("Invalid credentials"))
        else:
            messages.success(request, _("Error validating the form"))
    return render(request, "users/login/auth-signin.html", {"form": form})


@sensitive_post_parameters('password1', 'password2')
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get('email')
            user = CustomUser.objects.create_user(username=username, password=raw_password, email=email)
            user.save(using='users_db')
            login(request, user)
            messages.success(request, _("User created."))
            return redirect('users:index')
        else:
            messages.error(request, _("Form is not valid"))
    else:
        form = SignUpForm()

    return render(request, "users/login/auth-signup.html", {"form": form})


def do_login(request):
    if request.method != "POST":
        return HttpResponse("<h2>" + _("Method Not Allowed") + "</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'), database='users_db')
        if user is not None:
            login(request, user)
            return redirect('users:index')
        else:
            messages.error(request, _("Invalid Login Credentials!"))
            return redirect('users:login')


def logout_out(request):
    logout(request)
    return HttpResponseRedirect('/')


class UpdatePassword(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:user_profile')
    template_name = 'users/general_templates/change-password.html'
    success_message = _("The password has been changed.")


def user_profile(request):
    try:
        c_user = CustomUser.objects.using('users_db').get(id=request.user.id)
        context = {"c_user": c_user}
    except Exception as ex:
        logger.exception("Error in user profile, check it NOW: %s", str(ex))
        context = {}
    return render(request, 'users/general_templates/profile.html', context)


def profile_update(request):
    if request.method != "POST":
        messages.error(request, _("Invalid Method"))
        return redirect('users:user_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        about_me = request.POST.get('about_me')
        secret_word = request.POST.get('secret_word')
        email = request.POST.get('email')
        username = request.POST.get('username')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.secret_word = secret_word
            customuser.about_me = about_me
            customuser.email = email
            customuser.username = username
            customuser.save(using='users_db')
            messages.success(request, _("Profile Updated Successfully"))
            return redirect('users:user_profile')
        except CustomUser.DoesNotExist:
            messages.error(request, _("Failed to Update Profile"))
            return redirect('users:user_profile')
        except Exception as ex:
            messages.error(request, _("Error: ") + str(ex))
            return redirect('users:user_profile')
