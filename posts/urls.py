from django.conf.urls import url
from django.contrib import admin

from .views import (
    posts_list,
    posts_create,
    posts_detail,
    posts_update,
    posts_delete,
    about,
    postpreference,
    like_post,
    post_image,
    display_image,
    delete_image,
)

urlpatterns = [
    url(r'^$', posts_list, name='list'),
    url(r'^create/$', posts_create),
    url(r'^(?P<slug>[\w-]+)/$', posts_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', posts_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/image/delete-image/(?P<id>\d+)/$',
        delete_image, name='delete-image'),
    url(r'like_post/$', like_post, name='like_post'),
    url(r'^(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$',
        postpreference, name='postpreference'),
    url(r'^(?P<slug>[\w-]+)/mul-images/$', post_image, name='mul-images'),
    url(r'^(?P<slug>[\w-]+)/image/$',
        display_image, name='image')

]
