import logging
import time

import requests
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage

from crawler.models import CrawlerPages, CrawlerSites, CrawlQueue
from feedback.models import Problem
from .tasks import crawl_page_content, add_site_to_search
from .utils import get_domain_name, get_sub_domain_name
from core.models import ContentSearchIndex


logger = logging.getLogger("django")
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


crawler_pages = CrawlerPages.objects.using('crawler_db').all()
crawler_sites = CrawlerSites.objects.using('crawler_db').all()
problem = Problem.objects.using('feedback_db').all()
content_search = ContentSearchIndex.objects.using('search_db').all()


def update_crawl_q_status(url: str, status: int):
    cq = CrawlQueue.objects.using('crawler_db').filter(url=url).latest()
    cq.status = status
    print('cq', cq, status)
    cq.save()


def site_crawler(iii: int) -> None:
    """
    Getting an ID from the user of the site to crawl.
    The USP module creates the set/list of URLs. In for the loop page crawler, which visits every page and adds
    it to the database.
    Time sllep needs to wait for a response from the URL with content and add it to the DB.
    1-sec was not enough, 3-too much, 2-is good enough.
    :param iii:
    :return:
    """
    url = crawler_sites.get(id=iii).cr_url
    url_list = []
    tree = sitemap_tree_for_homepage(url)
    add_site_to_search(tree.url)
    try:
        for page in tree.all_pages():
            url_list.append(page.url)
            crawl_page_func(page.url)
            time.sleep(2)
    except ConnectionError as ce:
        logger.error("Crawler, crawl_views, site_crawler, Connection error: %s", str(ce))
    try:
        crawler_sites.filter(id=iii).update(
            sitemap_xml=tree,
            domain_name=get_domain_name(url),
            sub_domain_name=get_sub_domain_name(url),
            internal_links=url_list,
            status=1
        )
        update_crawl_q_status(url, status=1)
    except (TypeError, AttributeError) as type_attr_err:
        logger.error("Crawler, crawl_views, site_crawler; adding to db crawl site url %s ;"
                     "got exception TypeError, AttributeError %s", url, type_attr_err)
    except Exception as e:
        logger.error("Crawler, crawl_views, site_crawler; adding to db crawl site url %s ;"
                     "got Exception %s", url, str(e))
        problem.create(name="Site Crawler", error=(url, e))


def crawl_page_func(url: str) -> None:
    """
    Visiting URL address, visiting, adding to the database, or updating
    :param url:
    :return: None
    """
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "lxml")
    if not crawler_pages.filter(cr_url=url).exists():
        try:
            cp_c = crawler_pages.create(cr_url=url, cr_content=str(soup), status=3)
            cp_c.save()
            crawl_page_content(crid=cp_c.id)
            update_crawl_q_status(url, status=3)
        except Exception as ex:
            logger.error("Crawler, crawl_views, crawl_page_func, exception: %s", str(ex))
    else:
        try:
            cp = crawler_pages.filter(cr_url=url).update(cr_url=url, cr_content=str(soup), status=2)
            crawl_page_content(crid=cp.id)
            update_crawl_q_status(url, status=2)
        except Exception as ex:
            logger.error("Crawler, crawl_views, crawl_page_func, exception: %s", str(ex))
        logger.info("Crawler, crawl_views, crawl_page_func; updating db crawl site url %s", url)


def page_crawler(i: int) -> None:
    """
    :param i:
    :return:
    """
    url = crawler_pages.get(id=i).cr_url
    crawl_page_content(crid=i)
    return crawl_page_func(url)
