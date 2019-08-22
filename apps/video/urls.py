#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from django.conf.urls import url
from .views import VlogListView,VlogDetailView


app_name = 'video'

urlpatterns = [
    # path('', views.VlogListView.as_view(), name='list'),
    # url(r'^category/questions//$', VlogListView.as_view(), name='question'),

    # path('detail/<int:pk>', views.VlogDetailView.as_view(), name='detail'),
    url(r'^detail/(?P<pk>.*?)/$', VlogDetailView.as_view(), name='detail'),
    # url(r'^video/love/$', LoveView, name='love')
]