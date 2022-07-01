import json
import logging

from django.db.models import Q
from django.http import HttpResponse

from core.helpers.checks import autocom_check
from core.models import Autocomplete, SearchQueries

logger = logging.getLogger("django")


def autocomplete(request) -> HttpResponse:
    """Function for autocomplete search when user starts entering search query,
      this func. filter DB Autocomplete for matching term, if was found term its responding to ajax in search form """
    if request.is_ajax():
        q = request.GET.get('term', '')
        auto_com = Autocomplete.objects.using('search_db').filter(Q(name__icontains=q)).filter(status='approved')
        results = []
        for a in auto_com:
            a_json = a.name
            results.append(a_json)
        data = json.dumps(results)
        logger.info('Getting autocomplete from crawl site and added to Crawl Queue ')
    else:
        data = 'fail'
        logger.error('Fail to dump json data in autocomplete')
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def add_query(q: str) -> None:
    """Getting search query from view and adding to DB search results, we need those queries for providing autocomplete
     service
     """
    search_q = SearchQueries.objects.using('search_db').all()
    autocom_check()
    if q is not None and q != "":
        add_to_autocomplete(q)
        if not search_q.filter(query=q).exists():
            try:
                search_q.create(query=str(q), status=0).save(using='search_db')
            except Exception as e:
                logger.error(' %s', str(e))
        else:
            logger.info('add query else')
        logger.info('Received and filtered query from search, added to search results <query= %s>', q)
    else:
        logger.info('Received from search Empty query, Y not filtered?')


def add_to_autocomplete(q: str):
    auto_complete = Autocomplete.objects.using('search_db').all()
    if not auto_complete.filter(name=q).exists():
        try:
            auto_complete.create(name=q, status='pending').save(using='search_db')
        except Exception as ex:
            logger.exception("%s", str(ex))
    else:
        logger.info('add to autocomplete else')
