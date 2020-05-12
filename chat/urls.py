# chat/urls.py
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
