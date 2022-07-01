from django.urls import path
from . import views

app_name = 'backups'

urlpatterns = [
    path('all_db_backup/', views.all_db_backup, name="all_db_backup"),
    path('feedback_backup/', views.feedback_db_backup, name="feedback_backup"),
    path('users_backup/', views.users_db_backup, name="users_backup"),
    path('core_backup/', views.core_db_backup, name="core_backup"),
    path('analytics_backup/', views.analytics_db_backup, name="analytics_backup"),
    path('crawler_backup/', views.crawler_db_backup, name="crawler_backup"),
]
