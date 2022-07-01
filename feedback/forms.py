from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from .models import Feedback, Support, Contact


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ['status', 'results_was_not_helpful']
        fields = '__all__'
        labels = {'results_was_helpful': _('Results was helpful'),
                  'information_outdated': _('Information is outdated'),
                  'information_is_missing': _('Information is missing'),
                  'other_field': _('Other')
                  }

        widgets = {
            'other_field': widgets.TextInput(
                attrs={
                    'class': 'form-control'}),

            'results_was_helpful': widgets.Select(
                attrs={
                    'class': 'form-select form-select-sm"'
                }
            ),
    
            'information_outdated': widgets.Select(
                attrs={
                    'class': 'form-select form-select-sm"'
                }
            ),
            'information_is_missing': widgets.Select(
                attrs={
                    'class': 'form-select form-select-sm"'
                }
            ),
        }


class SupportForm(ModelForm):
    class Meta:
        model = Support

        labels = {'subject': _('Subject'), 'message': _('Message')}

        error_messages = {
            'subject': {
                'max_length': _("This subject is too long."),
                'required': _('This field is required')
            },
            'message': {
                'required': _('This field is required')
            },
        },
        widgets = {
            'subject': widgets.TextInput(
                attrs={'class': "form-control"}
            ),
            'message': widgets.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4'
                }
            )
        }
        fields = ['subject', 'message']


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        error_messages = {
            'subject': {
                'max_length': _("This subject is too long."),
                'required': _('This field is required')
            },
            'message': {
                'required': _('This field is required')
            },
            'email': {
                'required': _('This field is required')
            },
            'name': {
                'max_length': _("Name is too long."),
                'required': _('This field is required')
            },
        },
        widgets = {
            'subject': widgets.TextInput(
                attrs={'class': "form-control"}
            ),
            'message': widgets.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4'
                }
            ),
            'email': widgets.EmailInput(
                attrs={"class": "form-control"}
            ),
            'name': widgets.TextInput(
                attrs={"class": "form-control"}
            )
        }
        fields = ['name', 'email', 'subject', 'message']
