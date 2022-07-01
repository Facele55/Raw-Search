from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


USER_TYPE_DATA = [
    (1, _("Admin")), 
    (2, _("Staff")), 
    (3, _("Developer")), 
    (4, _("Common User"))
]
STATUS_DATA = [
    ('good', _("Good")),
    ('suspicious', _("Suspicious")),
    ('banned', _("Banned")),
]


class CustomUser(AbstractUser):
    user_type = models.CharField(default=4, choices=USER_TYPE_DATA, max_length=20)
    status = models.CharField(verbose_name=_("Status"),default='good', choices=STATUS_DATA, max_length=20)
    secret_word = models.CharField(blank=True, max_length=255)
    about_me = models.TextField(verbose_name=_("About me"), blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'users'
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ['-username']

    def __str__(self):
        return f"{self.get_full_name()}"
