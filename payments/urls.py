# payments/urls.py
from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'', views.HomePageView.as_view(), name='footer'),
    url(r'charge/', views.charge, name='charge'),  # new
]
