# from django.urls import path, include
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from chat.views import get_message
from chat.api import MessageModelViewSet, UserModelViewSet

router = DefaultRouter()
router.register('message', MessageModelViewSet, basename='message-api')
router.register('user', UserModelViewSet, basename='user-api')

urlpatterns = [
    url('api/v1/', include(router.urls)),

    url('^chat/$', login_required(
        TemplateView.as_view(template_name='chat/chat.html')), name='home'),
    url('^messages/$', get_message, name='chat_message')

    # url(r'^chat/$', user_logged_in, name='user_logged_in'),
    # url(r'^chat/$', user_logged_out, name='user_logged_out'),
]
