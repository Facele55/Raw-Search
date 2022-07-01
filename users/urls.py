from django.urls import path
from django.views.generic import TemplateView

from users import views, AdminView, StaffView, UserViews, DevelopViews
from users.LoginCheckMiddleWare import index


app_name = 'users'


urlpatterns = [
    # General Views
    path('', index, name="index"),
    path('login/', views.login_page, name="login"),
    path('do_login/', views.do_login, name="do_login"),
    path('logout/', views.logout_out, name="logout"),
    path('sign_up/', views.signup, name="sign_up"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('profile_update/', views.profile_update, name="profile_update"),
    path('change-password/', views.UpdatePassword.as_view(), name="update_password"),

    # Admin views
    path('admin_home/', AdminView.admin_home, name="admin_home"),
    path('edit_user_perm/<int:usr_id>', AdminView.EditPermUsers.as_view(), name="edit_user_perm"),
    path('manage_users/', AdminView.UserList.as_view(), name="manage_users"),

    path('search_to_autocomplete/', AdminView.SearchAutocomplete.as_view(), name="search_to_autocomplete"),
    path('autocomplete_approve/<int:res_id>/', AdminView.autocomplete_approve, name="autocomplete_approve"),
    path('autocomplete_reject/<int:res_id>/', AdminView.autocomplete_reject, name="autocomplete_reject"),

    path('feeds/', AdminView.FeedbackTable.as_view(), name="feeds"),
    path('support_table/', AdminView.SupportTable.as_view(), name="support_table"),
    path('problems/', AdminView.ProblemTable.as_view(), name="problems"),
    path('queue/', AdminView.CrawlQueueTable.as_view(), name="queue"),
    path('table_to_crawl_sites/', AdminView.CrawlSitesTable.as_view(), name="table_to_crawl_sites"),
    path('approve_site_crawl/<int:site_id>', AdminView.approve_site_crawl, name="approve_site_crawl"),
    path('approve_page_crawl/<int:page_id>', AdminView.approve_page_crawl, name="approve_page_crawl"),
    path('table_to_crawl_pages/', AdminView.CrawlPagesTable.as_view(), name="table_to_crawl_pages"),
    path('contact_table/', AdminView.ContactTable.as_view(), name="contact_table"),
    path('backups_table/', TemplateView.as_view(template_name='backups/backups.html'), name="backups_table"),
    path('add_to_q', AdminView.AddToQueueView.as_view(), name="add_to_q"),

    path('elasticsearch_status/', AdminView.is_elasticsearch_running, name="elasticsearch_status"),
    path('a_dash/', AdminView.account_dashboard, name="account_dashboard"),
    path('c_dash/', AdminView.crawler_dashboard, name="crawler_dashboard"),
    # Staff Views
    path('staff_home/', StaffView.staff_home, name="staff_home"),

    # Developer Views
    path('developer_home/', DevelopViews.developer_home, name="developer_home"),

    # User Views
    path('user_home/', UserViews.user_home, name="user_home"),

]
