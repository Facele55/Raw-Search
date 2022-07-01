from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),  # honeypot
    path('new_admin/', include('smuggler.urls')),  # adds button for load and dump data
    path('new_admin/backups/', include('dbbackup_ui.urls')),  # custom backups

    path('new_admin/', admin.site.urls),

    path('i18n/', include('django.conf.urls.i18n')),

    path('', include('core.urls')),
    path('a/', include('analytics.urls')),
    path('users/', include('users.urls')),
    path('feedback/', include('feedback.urls')),
    path('crawler/', include('crawler.urls')),
    path('backups/', include('backups.urls')),
]
