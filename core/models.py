from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


AUTOCOMPLETE_STATUSES = [
	('pending', _('Pending')),
	('approved', _('Approved')),
	('rejected', _('Rejected')),
]


class ContentSearchIndex(models.Model):
	"""Model for storing clean information from pages and search indexes,
	 """
	id = models.AutoField(primary_key=True)
	url = models.TextField()
	title = models.TextField(null=True)
	description = models.TextField(null=True)
	site_lang = models.TextField(null=True)
	site_content = models.TextField(null=True)
	keywords = models.TextField(null=True)
	crawler_fk_pages = models.IntegerField(null=True)
	status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Content Search Index"
		verbose_name_plural = "Content Search Indexes"

	def __str__(self):
		return self.url


class ImageSearchIndex(models.Model):
	"""
	Model for storing images, alt and url of every crawled image
	"""
	id = models.AutoField(primary_key=True)
	img_url = models.TextField()
	img_alt = models.TextField()
	status = models.IntegerField(default=0)
	crawler_fk_pages = models.IntegerField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Image Search Index"
		verbose_name_plural = "Image Search Indexes"

	def __str__(self):
		return f"{self.img_url}"


class VideoIndex(models.Model):
	"""Model for storing videos, alt and url of every crawled"""
	id = models.AutoField(primary_key=True)
	video_src_url = models.TextField()
	video_type = models.TextField()
	video_controls = models.TextField()
	status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Video Index"
		verbose_name_plural = "Video Indexes"

	def __str__(self):
		return f"{self.video_src_url}"


class SiteSearchIndex(models.Model):
	"""
	"""
	id = models.AutoField(primary_key=True)
	site_url = models.TextField()
	status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Site Search Index"
		verbose_name_plural = "Site Search Indexes"

	def __str__(self):
		return f"{self.site_url}"


class SearchQueries(models.Model):
	"""Model for storing search queries """
	id = models.AutoField(primary_key=True)
	query = models.TextField()
	status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.query}"

	class Meta:
		verbose_name = "Search Query"
		verbose_name_plural = "Search Queries"


class Autocomplete(models.Model):
	"""Model for storing terms for autocomplete """
	id = models.AutoField(primary_key=True)
	name = models.CharField(verbose_name=_("Name"), max_length=255)
	status = models.CharField(verbose_name=_("Status"), max_length=20, choices=AUTOCOMPLETE_STATUSES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "autocomplete"
		verbose_name_plural = "autocompletion"
