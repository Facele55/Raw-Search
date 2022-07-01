from django.contrib import admin
from .models import ContentSearchIndex, SearchQueries, Autocomplete, ImageSearchIndex, VideoIndex, SiteSearchIndex


class CoreAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'


admin.site.register(ContentSearchIndex, CoreAdmin)
admin.site.register(ImageSearchIndex, CoreAdmin)
admin.site.register(SearchQueries, CoreAdmin)
admin.site.register(Autocomplete, CoreAdmin)
admin.site.register(VideoIndex, CoreAdmin)
admin.site.register(SiteSearchIndex, CoreAdmin)
