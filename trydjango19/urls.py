from django.conf.urls import include, url
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.conf.urls.static import static
from django.contrib import admin
# import notifications.urls
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)
# from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from accounts.views import (
    login_view, register_view, logout_view, change_password, setting, password)
from posts.views import (posts_create, posts_delete, index,profilescreen,
                         posts_update, about, contact, get_user_profile, posts_list, post_image, display_image)
from django.contrib.sitemaps.views import sitemap
from trydjango19.sitemap import StaticViewSitemap, SnippetSitemap
sitemaps = {
    'static': StaticViewSitemap,
    'snippet': SnippetSitemap
}


urlpatterns = [
    url('^admin/', admin.site.urls),
    # url('chat/', include('chat.urls')),
    url('^$', posts_list, name='list'),
    url('', include('chat.urls')),
    url('^settings/$', setting, name='settings'),
    url('^settings/password/$', password, name='password'),
    url('^posts/', include(("posts.urls", "app_name"), namespace="posts")),
    url('^comments/', include(("comment.urls", "app_name"), namespace='comment')),
    url('^register/', register_view, name='register'),
    url('^login/', login_view, name='login'),
    url('^logout/', logout_view, name='logout'),
    url('^oauth/', include(('social_django.urls', "app_name"), namespace='social')),
    url('^create/$', posts_create, name='create'),
    url('^about/$', about, name='about'),
    url('^contact/$', contact, name='contact'),
    url('profile/$',
        get_user_profile, name='profile'),
    url('profilescreen/$',
        profilescreen, name='userprofile'),
    url('^password_change/$', change_password, name='change_pwd'),
    # url('inbox/notifications/',
    #     include(notifications.urls, namespace='notifications')),
    url('^sitemap.xml/$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    url('^robots.txt', lambda x: HttpResponse(
        "User-Agent: *\nDisallow:", content_type="text/plain"), name="robots_file"),
    path('password_reset/', PasswordResetView.as_view(success_url='done/'),
         name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        success_url='/reset/done/'), name="password_reset_confirm"),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    url('^api/v1/news/$', index, name='news'),
    # url(r'^ratings/', include(('star_ratings.urls', "app_name"),
    #                           namespace='ratings')),
    # url(r'', include('payments.urls')),  # new
]


if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
