#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import login_view, logout_view, register_view, profile_view, change_profile_view,create_article_view,\
    delete_article_view,update_article_view

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout', logout_view, name='logout'),
    url(r'^register/$', register_view, name='register'),
    url(r'^profile/$', profile_view, name='profile'),
    url(r'^profile/change/$', change_profile_view, name='change_profile'),
    url(r'^create/$', create_article_view, name='create'),
    url(r'^update/(?P<id>.*?)/$', update_article_view, name='update'),

    url(r'^delete/(?P<id>.*?)/$', delete_article_view, name='delete'),
]