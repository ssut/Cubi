#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('author.views',
    url(r'^introduce/$', 'introduce', name='introduce'),
    url(r'^agreement/$', 'agreement', name='agreement'),
    url(r'^index/$', 'index', name='index'),
)
