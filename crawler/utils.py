import logging
from urllib.error import HTTPError
from urllib.parse import urlparse


logger = logging.getLogger("django")


def get_domain_name(url: str) -> str:
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + "." + results[-1]
    except Exception as ex:
        logger.exception(ex)
        return ''


def get_sub_domain_name(url: str) -> str:
    try:
        return urlparse(url).netloc
    except HTTPError as http_error:
        logger.exception(http_error)
    except Exception as ex:
        logger.exception(ex)
        return ''
