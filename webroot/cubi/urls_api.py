#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'member.api.login'),
    url(r'^chapter/list/$', 'work.api.chapter_list'),
    url(r'^chapter/view/$', 'work.api.chapter_view'),
    url(r'^chapter/comment/list/$', 'work.api.chapter_comment_list'),
    url(r'^chapter/comment/add/$', 'work.api.chapter_comment_add'),

)