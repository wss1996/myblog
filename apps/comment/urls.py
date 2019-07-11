#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'comment'
urlpatterns = [
    # 发表评论
    url(r'^comment/article/(?P<pk>.*?)/$', views.post_comment, name='post_comment')
]