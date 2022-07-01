import logging

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from crawler.models import CrawlQueue, CrawlerSites, CrawlerPages

logger = logging.getLogger("django")
valid_url = ''


@csrf_exempt
def check_url_address_exist(request):
    url = request.POST.get("url")
    url_obj = CrawlQueue.objects.using('crawler_db').filter(url=url).exists()
    if url_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def add_url_to_crawl_queue(url: str, status: str, user: int):
    """
    Validate data, add url to DB Crawl Queue for later crawling,
    statuses: 1 = site, 2 = page
    """
    if status == 'site':
        try:
            site_q = CrawlQueue.objects.using('crawler_db').create(url=validate_url(url), page_site='site', added_by=user)
            site_q.save(using='crawler_db')
            logger.info('Crawler, services.add_url_to_crawl_queue to Crawl Queue status: %s \n  url: %s |'
                        ' status: 1 = site, 2 = page', status, url)
            check_new_site_urls(site_q.id, user)
        except Exception as e:
            logger.error('Adding to Crawl Queue, but smt went wrong, error %s', str(e))
    elif status == 'page':
        try:
            logger.info('Adding to Crawl Queue url: %s \n status: %s | status: 1 = site, 2 = page', url, status)
            page_q = CrawlQueue.objects.using('crawler_db').create(url=validate_url(url), page_site='page', added_by=user)
            page_q.save(using='crawler_db')
            logger.info('Adding to Crawl Queue <url %s', url)
            check_page_url_exist(page_q.id, user)
        except Exception as e:
            logger.error('Adding to Crawl Queue, but smt went wrong, error %s', str(e))
    else:
        logger.error('Crawler, services, Adding to Crawl Queue, wrong status, Security Alert (XSS)')


def check_page_url_exist(page_id: int, user: int):
    """
    This f-n checking for new urls which is not in DB Crawler Pages, if url not in DB crawler sites,
    than it will be added
    :param page_id:
    :param user:
    :return:
    """
    url = CrawlQueue.objects.using('crawler_db').get(id=page_id)
    url_obj = CrawlerPages.objects.using('crawler_db').all().filter(cr_url=url).exists()
    if url_obj:
        return print("Exist", url)
    else:
        CrawlerPages.objects.using('crawler_db').create(cr_url=url, added_by=user)
        return


def check_new_site_urls(site_id: int, user: int) -> None:
    """
    This f-n checking for new urls which is not in DB Crawler Sites, if url not in DB crawler sites,
    than it will be added
    :param site_id:
    :param user:
    :return:
    """
    url = CrawlQueue.objects.using('crawler_db').get(id=site_id)
    url_obj = CrawlerSites.objects.using('crawler_db').all().filter(cr_url=url).exists()
    if url_obj:
        return print("Exist")
    else:
        logger.info("Crawler, services, checking new site urls; url:  %s", url)
        logger.info("Crawler, services, checking new site urls; sent url %s to func. add_site_to_crawl for "
                    "adding to DB CrawlerSites", url)
        CrawlerSites.objects.using('crawler_db').create(cr_url=url, added_by=user)
        return


def validate_url(url: str) -> str:
    """
    Check if url is valid, if not: send to f-n _make_url_valid()
    :param url:
    :return:
    """
    validate = URLValidator()
    try:
        validate(url)
        return url
    except ValidationError as exception:
        logger.error("Crawler, services.validate_url; exception %s | url %s. \n"
                     "String is not valid URL, sent to validate ", exception, url)
        return _make_url_valid(url)


def _make_url_valid(url: str) -> str:
    """
    If validation was failed, url was sent here to make it valid.
    To url are adding scheme http:// and  than url returns to validate_url,
    else url are wrong or does not exist.
    :param url:
    :return:
    """
    global valid_url
    if not (url.startswith('http://') or url.startswith('https://')):
        valid_url = f'https://{url}'
        return valid_url
    else:
        pass
