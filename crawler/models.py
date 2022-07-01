from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class CrawlerPages(models.Model):
    """Model for storing raw data of crawled pages """
    id = models.AutoField(primary_key=True)
    cr_url = models.TextField()
    cr_content = models.TextField()
    status = models.IntegerField(default=0)
    added_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager

    class Meta:
        verbose_name = "Crawled Page"
        verbose_name_plural = "Crawled Pages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.cr_url}"


class CrawlerSites(models.Model):
    """Model for storing raw data of crawled sites,
     optional fields are using for storing additional data for which column was not assigned
     """
    id = models.AutoField(primary_key=True)
    cr_url = models.TextField()
    robot_txt = models.TextField()
    sitemap_xml = models.TextField()
    sitemap_rss = models.TextField()
    front_page_content = models.TextField()
    domain_name = models.TextField()
    sub_domain_name = models.TextField()
    internal_links = models.TextField()
    external_links = models.TextField()
    optional_field_1 = models.TextField(null=True)
    optional_field_2 = models.TextField(null=True)
    status = models.IntegerField(default=0)
    added_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager

    class Meta:
        verbose_name = "Crawler Site"
        verbose_name_plural = "Crawler Sites"

    def __str__(self):
        return f"{self.cr_url}"


PAGE_SITE = [
    ('page', _("Page")),
    ('site', _("Site")),
]


class CrawlQueue(models.Model):
    """Model for storing urls for future crawling """
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    page_site = models.CharField(default='empty', choices=PAGE_SITE, max_length=20)
    added_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager

    def __str__(self):
        return f"{self.url}"

    def get_added_by(self):
        user = CustomUser.objects.using('users_db').get(id=self.added_by)
        return f"{user}"

    class Meta:
        verbose_name = "Queue for Crawling"
        verbose_name_plural = "Queues for Crawling"
