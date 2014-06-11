# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'member.views',
    url(r'^favorites/add$', 'add_to_favorites', name='add_to_favorites'),
    url(r'^favorites/list$', 'get_favorites', name='get_favorites'),
    url(r'^connect/fb$', 'connect_facebook', name='connect_facebook'),
    url(r'^connect/fb/callback$', 'connect_facebook_callback',
        name='connect_facebook_callback'),
    url(r'^connect/fb/destroy$', 'disconnect_facebook',
        name='disconnect_facebook'),
    url(r'^signin/fb$', 'signin_with_facebook', name='signin_with_facebook'),
    url(r'^signin/fb/callback$', 'signin_with_facebook_callback',
        name='signin_with_facebook_callback'),

    url(r'delete/$', 'delete_account', name='delete_account')
)
