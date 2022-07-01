import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView


from django.shortcuts import render, redirect


from .forms import UrlCrawlQueueForm
from .services import add_url_to_crawl_queue
from .models import CrawlerPages, CrawlerSites, CrawlQueue
from core.models import ContentSearchIndex

logger = logging.getLogger("django")


class CrawlView(FormView):
    template_name = 'crawler/crawler.html'
    form_class = UrlCrawlQueueForm
    success_url = reverse_lazy('crawler:index')

    def form_valid(self, form):
        url = form.cleaned_data.get("url")
        filter_status = self.request.POST.get("filter")
        user = self.request.user.id
        add_url_to_crawl_queue(url=url, status=filter_status, user=user)
        messages.success(self.request, _('Thank You! ') + _('The URL address ') + url + _(' will be crawled soon'))
        logger.info("Feedback, CrawlView(FormView); got url %s and passed to services.add_to_q for checking and after "
                    "adding to DB CrawlQueue.Feedback", url)
        return HttpResponseRedirect(self.get_success_url())


def delete_page(request, cp_id: int):
    try:
        CrawlerPages.objects.using('crawler_db').get(id=cp_id).delete()
        messages.success(request, _("Deleted"))
    except Exception as ex:
        logger.exception("Error deleting page, %s", str(ex))
        messages.error(request, "Error" + str(ex))
    return redirect(request.META['HTTP_REFERER'])


def delete_site(request, cs_id: int):
    try:
        CrawlerSites.objects.using('crawler_db').get(id=cs_id).delete()
        messages.success(request, _("Deleted"))

    except Exception as ex:
        logger.exception("Error deleting site, %s", str(ex))
        messages.error(request, "Error" + str(ex))
    return redirect(request.META['HTTP_REFERER'])


def delete_from_queue(request, cq_id: int):
    try:
        CrawlQueue.objects.using('crawler_db').get(id=cq_id).delete()
        messages.success(request, _("Deleted"))
    except Exception as ex:
        logger.exception("Error deleting from queue, %s", str(ex))
        messages.error(request, "Error" + str(ex))
    return redirect(request.META['HTTP_REFERER'])


def complete_delete(request, cq_id: int):
    try:
        CrawlerPages.objects.using('crawler_db').get(id=cq_id).delete()
        ContentSearchIndex.objects.using('search_db').get(crawler_fk_pages=cq_id).delete()
        messages.success(request, _("Deleted"))
    except Exception as ex:
        logger.exception("Error deleting from queue, %s", str(ex))
        messages.error(request, "Error" + str(ex))
    return redirect(request.META['HTTP_REFERER'])