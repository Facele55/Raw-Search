from django.urls import path

from .views import *

app_name = 'feedback'


urlpatterns = [
    path('form/', FeedbackView.as_view(), name="form"),
    path('support/', SupportView.as_view(), name="support"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('mark_solved/<int:pr_id>/', mark_solved, name="mark_solved"),
    path('mark_solved_support/<int:pr_id>/', mark_solved_sup, name="mark_solved_support"),
]
