from django import forms
from django.contrib.auth.forms import UserCreationForm

from crawler.models import CrawlQueue
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, widgets


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : _("Username"),
                "class": "form-control",
                "type": "text"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("Email"),
                "class": "form-control",
                "type": "email"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Password"),
                "class": "form-control",
                "type": "password"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Repeat Password"),
                "class": "form-control",
                "type": "password"
            }
        ))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class EditUserPermForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['password', 'secret_word']
        labels = {'username': _("Username"),
                  "first_name": _("First Name"),
                  "last_name": _("Last Name"),
                  "email": _("Email"),
                  "user_type": _("User Type"),
                  "status": _("Status"),
                  "about_me": _("About me"),
                  }

        widgets = {
            'username': widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "disabled": "disabled"
                }
            ),
            "first_name": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "disabled": "disabled"
                }
            ),
            "last_name": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "disabled": "disabled"
                }
            ),
            "email": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "disabled": "disabled"
                }
            ),
            "user_type": widgets.Select(
                attrs={
                    'class': "form-control bg-white"
                }
            ),
            "status": widgets.Select(
                attrs={
                    'class': "form-control bg-white"
                }
            ),
            "last_login": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "disabled": "disabled"
                }
            ),
            'groups': widgets.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),
            'user_permissions': widgets.SelectMultiple(
                attrs={
                    "class": "form-control"
                }
            ),
            "date_joined": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "disabled": "disabled"
                }
            ),
            "about_me": widgets.Textarea(
                attrs={
                    "class": "form-control",
                    "disabled": "disabled"
                }
            )
            }


class QueueForm(ModelForm):
    class Meta:
        model = CrawlQueue
        exclude = ['status', 'added_by']
        fields = '__all__'
        widgets = {
            'url': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'url',
                }
            ),
        }
