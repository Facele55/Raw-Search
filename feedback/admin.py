from django.contrib import admin
from .models import Feedback, Support, Contact


class FeedbackAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Support, FeedbackAdmin)
admin.site.register(Contact, FeedbackAdmin)
