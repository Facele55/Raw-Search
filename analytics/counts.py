import logging
from django.db.models import Count, Q

from core.models import ContentSearchIndex, ImageSearchIndex, SearchQueries, Autocomplete, VideoIndex, SiteSearchIndex
from crawler.models import CrawlerSites, CrawlerPages, CrawlQueue
from feedback.models import Feedback, Support, Problem
from users.models import CustomUser

from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate

logger = logging.getLogger("django")


def count_crawler_sites() -> int:
	"""
	F-n for counting total amount records for CrawlerSites
	:return:
	"""
	try:
		total = CrawlerSites.objects.using('crawler_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_crawler_pages() -> int:
	"""
	F-n for counting total amount records for CrawlerPages
	:return:
	"""
	try:
		total = CrawlerPages.objects.using('crawler_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_crawler_queue() -> int:
	"""
	F-n for counting total amount records for CrawlQueue
	:return:
	"""
	try:
		total = CrawlQueue.objects.using('crawler_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_content_search_index() -> int:
	"""
	F-n for counting total amount records for ContentSearchIndex
	:return:
	"""
	try:
		total = ContentSearchIndex.objects.using('search_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_image_search_index():
	"""
	F-n for counting total amount records for ImageSearchIndex
	:return:
	"""
	try:
		total = ImageSearchIndex.objects.using('search_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_search_queries() -> int:
	"""
	F-n for counting total amount records for SearchQueries
	:return:
	"""
	try:
		total = SearchQueries.objects.using('search_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_autocomplete() -> int:
	"""
	F-n for counting total amount records for Autocomplete
	:return:
	"""
	try:
		total = Autocomplete.objects.using('search_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_site_search_index() -> int:
	"""
	F-n for counting total amount records for SiteSearchIndex
	:return:
	"""
	try:
		total = SiteSearchIndex.objects.using('search_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_video_index() -> int:
	"""
	F-n for counting total amount records for VideoIndex
	:return:
	"""

	try:
		total = VideoIndex.objects.using('search_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_feedback() -> int:
	"""
	F-n for counting total amount records for Feedback
	:return:
	"""
	try:
		total = Feedback.objects.using('feedback_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_support() -> int:
	"""
	F-n for counting total amount records for Support
	:return:
	"""
	try:
		total = Support.objects.using('feedback_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_users_admin() -> int:
	"""
	F-n for counting total amount records of CustomUser with user type = 1 (admin)
	:return:
	"""
	try:
		total = CustomUser.objects.using('users_db').all().filter(Q(user_type=1)).aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_users_staff() -> int:
	"""
	F-n for counting total amount records of CustomUser with user type = 2 (staff)
	:return:
	"""
	try:
		total = CustomUser.objects.using('users_db').all().filter(Q(user_type=2)).aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_users_developer() -> int:
	"""
		F-n for counting total amount records of CustomUser with user type = 3 (developer)
	:return:
	"""
	try:
		total = CustomUser.objects.using('users_db').all().filter(Q(user_type=3)).aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_users_user() -> int:
	"""
			F-n for counting total amount records of CustomUser with user type = 4 (regular user)
	:return:
	"""
	try:
		total = CustomUser.objects.using('users_db').all().filter(Q(user_type=4)).aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_autocomplete_pending() -> int:
	"""
	F-n for counting total amount records for Autocomplete which has status = 0 (pending)
	:return:
	"""
	try:
		total = Autocomplete.objects.using('search_db').all().filter(Q(status='pending')).aggregate(Count('id'))[
			'id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_autocomplete_approved() -> int:
	"""
	F-n for counting total amount records for Autocomplete which has status = 1 (approved)
	:return:
	"""
	try:
		total = Autocomplete.objects.using('search_db').all().filter(Q(status='approved')).aggregate(Count('id'))[
			'id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_autocomplete_rejected() -> int:
	"""
	F-n for counting total amount records for Autocomplete which has status = 2 (rejected)
	:return:
	"""
	try:
		total = Autocomplete.objects.using('search_db').all().filter(Q(status='rejected')).aggregate(Count('id'))[
			'id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_problem() -> int:
	"""
	F-n for counting total amount records for Problem
	:return:
	"""
	try:
		total = Problem.objects.using('feedback_db').all().aggregate(Count('id'))['id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_problem_solved() -> int:
	"""
	F-n for counting total amount records for problem with status = 1 (solved)
	:return:
	"""
	try:
		total = Problem.objects.using('feedback_db').all().filter(Q(status='solved')).aggregate(Count('id'))[
			'id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_problem_pending() -> int:
	"""
	F-n for counting total amount records for problem with status = 0 (pending)
	:return:
	"""
	try:
		total = Problem.objects.using('feedback_db').all().filter(Q(status='pending')).aggregate(Count('id'))[
			'id__count']
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total


def count_users_by_year():
	try:
		total = CustomUser.objects.using('users_db').all().annotate(year=ExtractYear('date_joined')).order_by(
			'year').values('year').annotate(**{'total': Count('year')})
		return total
	except Exception as ex:
		logger.exception("Analytics, counters, exception %s", ex)
		total = 0
		return total
