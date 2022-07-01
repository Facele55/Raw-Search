from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _
from .models import CrawlQueue


class UrlCrawlQueueForm(ModelForm):
    class Meta:
        model = CrawlQueue
        exclude = ['status', 'added_by', 'page_site']
        fields = '__all__'
        widgets = {
            'url': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'url',
                    'value': 'https://',
                    'placeholder': _('Type here address for crawling' + '...')
                }
            )
        }
