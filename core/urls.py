from django.urls import path
from django.views.generic import TemplateView

from core.helpers.helpers import autocomplete
from core.views import *

app_name = 'core'

urlpatterns = [
	path('', TemplateView.as_view(template_name='core/index.html'), name="index"),
	path('search/', SearchList.as_view(), name="search"),
	path('image/', ImageList.as_view(), name="search_img"),
	path('etc/', EtcList.as_view(), name="search_etc"),

	path('docs/', TemplateView.as_view(template_name='core/docs.html'), name="docs"),
	path('privacy_policy/', TemplateView.as_view(template_name='core/privacy_policy.html'), name="privacy_policy"),
	path('about/', TemplateView.as_view(template_name='core/about.html'), name="about"),
	path('autocomplete/', autocomplete, name="autocomplete"),

	# errors
	path('404/', TemplateView.as_view(template_name='core/errors/404.html'), name="404"),
	path('403/', TemplateView.as_view(template_name='core/errors/403.html'), name="403"),
	path('500/', TemplateView.as_view(template_name='core/errors/500.html'), name="500"),
	path('503/', TemplateView.as_view(template_name='core/errors/503.html'), name="503"),
	path('504/', TemplateView.as_view(template_name='core/errors/504.html'), name="504"),
	path('maintenance/', TemplateView.as_view(template_name='core/errors/maintenance.html'), name="maintenance"),
]
