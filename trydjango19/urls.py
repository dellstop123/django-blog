from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from accounts.views import (
    login_view, register_view, logout_view, change_password, setting,password)
from posts.views import (posts_create, posts_delete,
                         posts_update, about, contact, get_user_profile, posts_list,)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', posts_list, name='list'),
    url(r'^settings/$', setting, name='settings'),
    url(r'^settings/password/$', password, name='password'),
    url(r'^posts/', include("posts.urls", namespace="posts")),
    url(r'^comments/', include("comment.urls", namespace='comment')),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^create/$', posts_create, name='create'),
    url(r'^delete/$', posts_delete, name='delete'),
    url(r'^about/$', about, name='about'),
    url(r'^contact/$', contact, name='contact'),
    url(r'profile/$',
        get_user_profile, name='profile'),
    url(r'^password_change/$', change_password, name='change_pwd'),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
