#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('member.views',
    url(r'^favorites/add$', 'add_to_favorites', name='add_to_favorites'),
)