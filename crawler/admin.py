from django.contrib import admin

from crawler.models import CrawlerSites, CrawlerPages, CrawlQueue


class CrawlerAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'


admin.site.register(CrawlerPages, CrawlerAdmin)
admin.site.register(CrawlerSites, CrawlerAdmin)
admin.site.register(CrawlQueue, CrawlerAdmin)
