import logging

from core.models import Autocomplete, SearchQueries

logger = logging.getLogger("django")


def autocom_check():
    """Autocomplete check, when user submitting search query its adding to DB search Results,
    here func. are filtering and adding to DB Autocomplete unique queries"""
    try:
        ac = Autocomplete.objects.using('search_db').all()
        sr = SearchQueries.objects.using('search_db').all()
        for i in sr.filter(status=0):
            if i.status == 0:
                if not ac.filter(name=i.query):
                    ac.create(name=i.query).save(using='search_db')
                else:
                    i.status = 1
                    i.save(using='search_db')
            else:
                logger.info("Core, helpers, autocom_check; else statement")
    except Exception as e:
        logger.error('Autocomplete check error %s', str(e))
