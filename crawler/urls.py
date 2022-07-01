from django.urls import path

from crawler import services
from crawler.views import CrawlView, delete_page, delete_site, delete_from_queue, complete_delete


app_name = 'crawler'


urlpatterns = [
    path('', CrawlView.as_view(), name="index"),
    path('check_url_address_exist/', services.check_url_address_exist, name="check_url_address_exist"),
    path('delete_page/<int:cp_id>/', delete_page, name="delete_page"),
    path('delete_site/<int:cs_id>/', delete_site, name="delete_site"),
    path('delete_from_q/<int:cq_id>/', delete_from_queue, name="delete_from_queue"),
    path('complete_delete/<int:cq_id>/', complete_delete, name="complete_delete"),
]
