# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'administrator.views',

    url(r'^$', 'index', name='index'),
    url(r'^convert/(\d+)/(\w+)/$', 'convert', name='convert'),

    url(r'^work/list/$', 'work_list', name='work_list'),

    url(r'^crawl/list/$', 'crawl_list', name='crawl_list'),
    url(r'^crawl/list/new$', 'add_crawl_list', name='add_crawl_list'),
    url(r'^crawl/list/get$', 'get_crawl_list', name='get_crawl_list'),
    url(r'^crawl/list/toggle$', 'toggle_crawl_enabled',
        name='toggle_crawl_enabled'),
    url(r'^crawl/start$', 'crawl_instantly', name='crawl_instantly'),

    url(r'^user/search$', 'search_user', name='search_user'),
)
