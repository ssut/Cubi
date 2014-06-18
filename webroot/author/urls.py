# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'author.views',

    url(r'^(\d+)/$', 'info', name='info'),
    url(r'^introduce/$', 'introduce', name='introduce'),
    url(r'^agreement/$', 'agreement', name='agreement'),
    url(r'^index/$', 'index', name='index'),
    url(r'^update/$', 'update', name='update_info'),
    url(r'^work/add/$', 'addwork', name='addwork'),
    url(r'^work/(\d+)/edit', 'editwork', name='editwork'),
    url(r'^work/(\d+)/add_chapter', 'addchapter', name='addchapter'),
    url(r'^work/add/type/$', 'addwork_select_type',
        name='addwork_select_type'),
    url(r'^work/add/info/$', 'addwork_info', name='addwork_info'),
)
