from elasticsearch import Elasticsearch
import logging
import time
from urllib import request

from django.views.generic import ListView
from elasticsearch_dsl import Q

from core.models import ContentSearchIndex, ImageSearchIndex, SiteSearchIndex
from .documents import ContentSearchDocument, ImageSearchDocument, SiteSearchDocument
from .helpers.helpers import add_query

logger = logging.getLogger("django")


class SearchList(ListView):
	template_name = 'core/search/serp_all.html'
	paginate_by = 10
	count = 0
	time_queryset = 0

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['count'] = self.count or 0
		context['query'] = self.request.GET.get('q', '')
		context['results'] = self.get_queryset()
		context['total'] = self.time_queryset
		context['site'] = site_results(self.request.GET.get('q', ''))
		add_query(q=self.request.GET.get('q'))
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		query = request.GET.get('q', '')
		lang_code = self.request.LANGUAGE_CODE
		if query is not None and query != "":
			try:
				start_time = time.time()
				client = Elasticsearch()
				new_results = ContentSearchDocument.search(using=client).extra(size=+10000).query(
					Q("multi_match", query=query, fields=['title', 'site_content']))
				#  .sort('site_lang') - not working
				# .sort({"_score": {"order": "desc"}})
				response = new_results.execute()
				end_time = time.time()
				self.count = response.hits.total.value  # since qs is actually a list
				self.time_queryset = end_time - start_time
				return response if response is not None else []
			except (ConnectionRefusedError, ConnectionError, BaseException) as err:
				logger.exception("Search List | Exception: ConnectionError, TypeError, AttributeError %s", str(err))
				return []
			except Exception as ex:
				logger.exception("Search List | Exception: %s", str(ex))
			return []

		else:
			return ContentSearchIndex.objects.using('search_db').none()


def site_results(query: str):
	if query is not None and query != "":
		try:
			site_result = SiteSearchDocument.search().extra(size=+10000).query("prefix", site_url=query)
			site_response = site_result.execute()
			return site_response if site_response is not None else []
		except (ConnectionRefusedError, ConnectionError, BaseException) as err:
			logger.exception(
				"Site Search Results | Exception: ConnectionRefusedError, ConnectionError, BaseException %s", str(err))
			return []
		except Exception as ex:
			logger.exception(request, "Site Search Results, Exception %s", str(ex))
			return []
	else:
		return SiteSearchIndex.objects.using('search_db').none()


class ImageList(ListView):
	template_name = 'core/search/serp_images.html'
	paginate_by = 10
	count = 0
	time_queryset = 0

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['count'] = self.count or 0
		context['query'] = self.request.GET.get('q', '')
		context['results'] = self.get_queryset()
		context['total'] = self.time_queryset
		add_query(q=self.request.GET.get('q'))
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		query = request.GET.get('q', '')
		if query is not None and query != "":
			try:
				start_time = time.time()
				img_search = ImageSearchDocument.search().extra(size=+10000).query("match", img_alt=query)
				results = img_search.execute()
				print(results)
				end_time = time.time()
				self.count = len(results)
				self.time_queryset = end_time - start_time
				return results if results is not None else []
			except (ConnectionRefusedError, ConnectionError, BaseException) as err:
				logger.exception("Image List | Exception: ConnectionRefusedError, ConnectionError, BaseException %s",
				                 str(err))
				return []
			except Exception as ex:
				logger.exception(request, "Image List, Exception %s", str(ex))
				return []
		else:
			return ImageSearchIndex.objects.using('search_db').none()


class EtcList(ListView):
	template_name = 'core/search/serp_etc.html'
	paginate_by = 10
	count = 0
	time_queryset = 0

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['count'] = self.count or 0
		context['query'] = self.request.GET.get('q', '')
		context['results'] = self.get_queryset()
		context['total'] = self.time_queryset
		add_query(q=self.request.GET.get('q'))
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		query = request.GET.get('q', '')
		if query is not None and query != "":
			try:
				start_time = time.time()
				results = ContentSearchDocument.search().extra(size=+10000).query("match", site_content=query)
				response = results.execute()
				end_time = time.time()
				self.count = response.hits.total.value  # since qs is actually a list
				self.time_queryset = end_time - start_time
				return response if response is not None else []
			except (ConnectionRefusedError, ConnectionError, BaseException) as err:
				logger.exception("Etc List | Exception: ConnectionRefusedError, ConnectionError, BaseException %s",
				                 str(err))
				return []
			except Exception as ex:
				logger.exception(request, "Etc List, Exception %s", str(ex))
				return []
		else:
			return ContentSearchIndex.objects.using('search_db').none()
