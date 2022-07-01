from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


CHOICES = [
    ('yes', _('YES')),
    ('no', _('NO')),
]
PROBLEM_SUPPORT_STATUSES = [
        ('pending', _('Pending')),
        ('solved', _('Solved')),
]
FEEDBACK_STATUSES = [
        ('pending', _('Pending')),
        ('seen', _('Seen')),
]


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    results_was_helpful = models.CharField(choices=CHOICES, default='empty', blank=True, max_length=3)
    information_outdated = models.CharField(choices=CHOICES, default='empty', blank=True, max_length=3)
    information_is_missing = models.CharField(choices=CHOICES, default='empty', blank=True, max_length=3)
    other_field = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = models.Manager

    class Meta:
        app_label = 'feedback'
        verbose_name = "feedback"
        verbose_name_plural = "feedbacks"
        ordering = ['-timestamp']
        db_table = "feedback"

    def __str__(self):
        return f"{self.id}"


class Support(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255, verbose_name=_("User"))
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    status = models.CharField(verbose_name=_("Status"), max_length=20, choices=PROBLEM_SUPPORT_STATUSES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = models.Manager

    class Meta:
        app_label = 'feedback'
        verbose_name = "support"
        verbose_name_plural = "support"
        ordering = ['-timestamp']
        db_table = "support"

    def __str__(self):
        return f"{self.subject}"


class Problem(models.Model):
    """
    Model for storing problem errors. All errors had been added to logger, additionally the most crucial errors,
    problems are going to be added here to notify admins
    """
    id = models.AutoField(primary_key=True)
    name = models.TextField(verbose_name=_("Name"))
    error = models.TextField(verbose_name=_("Error"))
    status = models.CharField(verbose_name=_("Status"), max_length=20, choices=PROBLEM_SUPPORT_STATUSES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'feedback'
        verbose_name = "problem"
        verbose_name_plural = "problems"
        db_table = "problem"

    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    """
    Contact Form
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'feedback'
        verbose_name = "contact"
        verbose_name_plural = "contacts"
        ordering = ['-timestamp']
        db_table = "contact"

    def __str__(self):
        return f"{self.name} - {self.subject}"
