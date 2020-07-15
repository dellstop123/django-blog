from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import notifications.urls
# from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from accounts.views import (
    login_view, register_view, logout_view, change_password, setting, password)
from posts.views import (posts_create, posts_delete,
                         posts_update, about, contact, get_user_profile, posts_list, post_image, display_image)
from django.contrib.sitemaps.views import sitemap
from trydjango19.sitemap import StaticViewSitemap
sitemaps = {
    'static': StaticViewSitemap
}


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url('chat/', include('chat.urls')),
    url(r'^$', posts_list, name='list'),
    url(r'', include('chat.urls')),
    url(r'^settings/$', setting, name='settings'),
    url(r'^settings/password/$', password, name='password'),
    url(r'^posts/', include(("posts.urls", "app_name"), namespace="posts")),
    url(r'^comments/', include(("comment.urls", "app_name"), namespace='comment')),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^oauth/', include(('social_django.urls', "app_name"), namespace='social')),
    url(r'^create/$', posts_create, name='create'),
    url(r'^about/$', about, name='about'),
    url(r'^contact/$', contact, name='contact'),
    url(r'profile/$',
        get_user_profile, name='profile'),
    url(r'^password_change/$', change_password, name='change_pwd'),
    url(r'inbox/notifications/',
        include(notifications.urls, namespace='notifications')),
    url(r'^sitemap.xml/$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    # url(r'^ratings/', include(('star_ratings.urls', "app_name"),
    #                           namespace='ratings')),
    # url(r'', include('payments.urls')),  # new
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
