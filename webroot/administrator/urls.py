#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
)
urlpatterns += patterns('administrator.views',
    url(r'^$', 'index', name='index'),
    url(r'^wait_convert_list/', 'wait_convert_list', name='wait_convert_list'),
    url(r'^convert/(\d+)/(\w+)/$', 'convert', name='convert'),

    url(r'^work/list/$', 'work_list', name='work_list'),

    url(r'^crawl/list/$', 'crawl_list', name='crawl_list'),
)