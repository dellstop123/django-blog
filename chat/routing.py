# chat/routing.py
from django.conf.urls import url
from .consumer import ChatConsumer

websocket_urlpatterns = [
    url(r'^ws$', ChatConsumer),
]
