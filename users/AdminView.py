import django_filters
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, FormView

from analytics.counts import *
from core.models import Autocomplete
from crawler.crawl_views import site_crawler, page_crawler
from crawler.models import CrawlerPages, CrawlerSites, CrawlQueue
from feedback.models import Feedback, Support, Problem, Contact
from rawsearch.settings import ELASTICSEARCH_DSL
from .forms import EditUserPermForm, QueueForm
from .models import CustomUser

logger = logging.getLogger("django")
RESULTS_PER_PAGE = 10


@login_required(login_url='users:login')
def admin_home(request):
    feedback = [count_feedback(), count_support()]
    feedback_sum = sum(feedback)
    core = [count_autocomplete(), count_content_search_index(), count_image_search_index(), count_video_index(),
            count_site_search_index(), count_search_queries()]
    core_sum = sum(core)

    context = {
        "count_crawler_sites": count_crawler_sites,
        "count_crawler_pages": count_crawler_pages,
        "count_crawler_queue": count_crawler_queue,

        "count_content_search_index": count_content_search_index,
        "count_image_search_index": count_image_search_index,
        "count_video_index": count_video_index,
        "count_site_search_index": count_site_search_index,
        "count_search_queries": count_search_queries,
        "count_autocomplete": count_autocomplete,

        "count_support": count_support,
        "count_feedback": count_feedback,

        "count_autocomplete_approved": count_autocomplete_approved,
        "count_autocomplete_pending": count_autocomplete_pending,
        "count_autocomplete_rejected": count_autocomplete_rejected,

        "count_problem": count_problem,
        "count_problem_pending": count_problem_pending,
        "count_problem_solved": count_problem_solved,

        "support": Support.objects.using('feedback_db').all().filter(status='pending').order_by('-timestamp')[:3],
        "problem": Problem.objects.using('feedback_db').all().filter(status='pending').order_by('-timestamp')[:3],

        "feedback_sum": feedback_sum,
        "core_sum": core_sum,
    }
    return render(request, 'users/admin_templates/index.html', context)


def account_dashboard(request):
    users_list = [count_users_admin(), count_users_developer(), count_users_staff(), count_users_user()]
    users_sum = sum(users_list)
    context = {
        "count_users_admin": count_users_admin,
        "count_users_developer": count_users_developer,
        "count_users_staff": count_users_staff,
        "count_users_user": count_users_user,
        "users_sum": users_sum,
        "users_by_year": count_users_by_year,

    }
    return render(request, 'users/admin_templates/users_dashboard.html', context)


def crawler_dashboard(request):
    sites_by_year = CrawlerSites.objects.using('crawler_db').all().annotate(year=ExtractYear('created_at')).values(
        'year').annotate(count=Count('id')).values('year', 'count')
    crawler = [count_crawler_pages(), count_crawler_queue(), count_crawler_sites()]
    crawler_sum = sum(crawler)
    context = {
        "count_crawler_sites": count_crawler_sites,
        "count_crawler_pages": count_crawler_pages,
        "count_crawler_queue": count_crawler_queue,

        "crawler_sum": crawler_sum,
        "sites_by_year": sites_by_year,
    }
    return render(request, 'users/admin_templates/crawler_dashboard.html', context)


class FeedbackTable(ListView):
    template_name = "users/admin_templates/feedbacks.html"
    model = Feedback
    ordering = '-id'
    paginate_by = RESULTS_PER_PAGE


class ContactTable(ListView):
    template_name = "users/admin_templates/contact_entries.html"
    model = Contact
    ordering = '-timestamp'
    paginate_by = RESULTS_PER_PAGE


class ProblemFilter(django_filters.FilterSet):
    """
    Applying filters for Problem
    """
    class Meta:
        model = Problem
        fields = ['status']


class ProblemTable(ListView):
    template_name = "users/admin_templates/problem_table.html"
    model = Problem
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProblemTable, self).get_context_data()
        context['query'] = self.request.GET.get('status', '')
        context['filter'] = ProblemFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = Problem.objects.using('feedback_db').filter().order_by('status')
        return ProblemFilter(self.request.GET, queryset=queryset).qs


class UserList(ListView):
    template_name = "users/admin_templates/manage_users_template.html"
    model = CustomUser
    ordering = '-date_joined'
    paginate_by = RESULTS_PER_PAGE


class EditPermUsers(UpdateView):
    model = CustomUser
    template_name = 'users/admin_templates/edit_user_perm.html'
    success_url = reverse_lazy('users:account_dashboard')
    pk_url_kwarg = 'usr_id'
    form_class = EditUserPermForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Updated'))
        return redirect(self.get_success_url())


class CrawlSitesTable(ListView):
    template_name = "users/admin_templates/table_to_crawl_sites.html"
    model = CrawlerSites
    ordering = '-created_at'
    paginate_by = RESULTS_PER_PAGE


class CrawlPagesTable(ListView):
    template_name = "users/admin_templates/table_to_crawl_pages.html"
    model = CrawlerPages
    ordering = "-created_at"
    paginate_by = RESULTS_PER_PAGE


class CrawlQueueTable(ListView):
    template_name = "users/admin_templates/crawl_queue.html"
    model = CrawlQueue
    ordering = "-created_at"
    paginate_by = RESULTS_PER_PAGE


class AddToQueueView(FormView):
    model = CrawlQueue
    form_class = QueueForm
    template_name = "users/admin_templates/add_to_queue.html"
    success_url = reverse_lazy('users:queue')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.added_by = self.request.user.id
        f.save()
        form.save_m2m()
        return redirect(self.get_success_url())


class AutocompleteFilter(django_filters.FilterSet):
    """
    Applying filters for Autocomplete
    """
    class Meta:
        model = Autocomplete
        fields = ['status', ]


class SearchAutocomplete(ListView):
    template_name = "users/admin_templates/confirm_autocomplete.html"
    model = Autocomplete
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(SearchAutocomplete, self).get_context_data()
        context['query'] = self.request.GET.get('status', '')
        context['filter'] = (AutocompleteFilter(self.request.GET, queryset=self.get_queryset()))
        context['paginate_by'] = (self.request.GET.get('paginate_by'))
        return context

    def get_queryset(self):
        queryset = Autocomplete.objects.using('search_db').filter().order_by('status')
        return AutocompleteFilter(self.request.GET, queryset=queryset).qs

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)


class SupportTable(ListView):
    template_name = "users/admin_templates/supports_table.html"
    model = Support
    ordering = "timestamp"
    paginate_by = RESULTS_PER_PAGE


def approve_site_crawl(request, site_id: int):
    try:
        site = CrawlerSites.objects.using('crawler_db').get(id=site_id)
        site_crawler(iii=site.id)
        messages.success(request, _("Crawled"))
        return redirect(request.META['HTTP_REFERER'])
    except CrawlerSites.DoesNotExist:
        messages.error(request, _("Site Does Not Exist"))
        logger.info("Users, AdminView, approve_site_crawl, site id %d DoesNotExist", site_id)
        return redirect('users:table_to_crawl_sites')
    except Exception as ex:
        logger.exception("Users, AdminView, approve_site_crawl, exception %s", ex)
        messages.error(request, _("Error: ") + str(ex))
        return redirect(request.META['HTTP_REFERER'])


def approve_page_crawl(request, page_id: int):
    try:
        page = CrawlerPages.objects.using('crawler_db').get(id=page_id)
        page_crawler(page.id)
        messages.success(request, _("Crawled"))
        return redirect(request.META['HTTP_REFERER'])
    except CrawlerPages.DoesNotExist:
        messages.error(request, _("Page Does Not Exist"))
        logger.error("Users, AdminView, approve_page_crawl, page id %d DoesNotExist", page_id)
        return redirect('users:table_to_crawl_pages')
    except Exception as ex:
        logger.exception("Users, AdminView, approve_page_crawl, exception %s", ex)
        messages.error(request, _("Error: ") + str(ex))
        return redirect(request.META['HTTP_REFERER'])


def autocomplete_approve(request, res_id: int):
    try:
        auto_c = Autocomplete.objects.using('search_db').get(id=res_id)
        auto_c.status = 'approved'
        auto_c.save()
        messages.success(request, _("Approved"))
    except Exception as ex:
        messages.error(request, _("Error: ") + str(ex))
    return redirect('users:search_to_autocomplete')


def autocomplete_reject(request, res_id: int):
    try:
        result = Autocomplete.objects.using('search_db').get(id=res_id)
        result.status = 'rejected'
        result.save()
        messages.error(request, _("Rejected"))
    except Exception as ex:
        messages.error(request, _("Error: ") + str(ex))
    return redirect(request.META['HTTP_REFERER'])


def is_elasticsearch_running(request) -> JsonResponse:
    if request.method == 'GET':
        try:
            res = requests.get("http://" + ELASTICSEARCH_DSL['default']['hosts'])
            print(ELASTICSEARCH_DSL['default']['hosts'])
            if res.status_code == 200:
                return JsonResponse({'status': "running"})
        except (ConnectionRefusedError, ConnectionError, BaseException):
            return JsonResponse({'status': "inactive"})
        except Exception as e:
            logger.exception("is_elasticsearch_running(), exception %s", e)
    else:
        return JsonResponse({'status': "wrong_request"})
