from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import ContentSearchIndex, ImageSearchIndex, SiteSearchIndex


@registry.register_document
class ContentSearchDocument(Document):
	class Index:
		# Name of the Elasticsearch index
		name = 'content_search_index'
		# See Elasticsearch Indices API reference for available settings
		settings = {'number_of_shards': 1, 'number_of_replicas': 0, }

	class Django:
		model = ContentSearchIndex  # The model associated with this Document

		# The fields of the model you want to be indexed in Elasticsearch
		fields = ['id', 'url', 'title', 'description', 'site_lang', 'site_content', 'keywords']


@registry.register_document
class ImageSearchDocument(Document):
	class Index:
		# Name of the Elasticsearch index
		name = 'image_search_index'
		# See Elasticsearch Indices API reference for available settings
		settings = {'number_of_shards': 1, 'number_of_replicas': 0, }

	class Django:
		model = ImageSearchIndex  # The model associated with this Document

		# The fields of the model you want to be indexed in Elasticsearch
		fields = ['id', 'img_alt', 'img_url']


@registry.register_document
class SiteSearchDocument(Document):
	class Index:
		# Name of the Elasticsearch index
		name = 'site_search_index'
		# See Elasticsearch Indices API reference for available settings
		settings = {'number_of_shards': 1, 'number_of_replicas': 0, }

	class Django:
		model = SiteSearchIndex  # The model associated with this Document

		# The fields of the model you want to be indexed in Elasticsearch
		fields = ['id', 'site_url']
