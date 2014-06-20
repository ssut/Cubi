# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^version/$', 'tinicube.api.version'),
)
urlpatterns += patterns(
    'member.api',
    url(r'^login/$', 'login'),
    url(r'^signup/$', 'signup'),
    url(r'^author/info/$', 'author_info'),
    url(r'^author/list/$', 'all_author_list'),
    url(r'^author/list/favorite/$', 'favorite_author_list'),
)

urlpatterns += patterns(
    'work.api',
    url(r'^tinicube/chapter/recentupdatelist/$', 'recent_update_chapter_list'),
    url(r'^tinicube/work/newlist/$', 'new_work_list'),
    url(r'^tinicube/work/poplist/$', 'popular_work_list'),
    url(r'^tinicube/author/newlist/$', 'new_author_list'),
    url(r'^tinicube/author/poplist/$', 'popular_author_list'),

    url(r'^work/list/$', 'work_list'),
    url(r'^work/list/favorite/$', 'work_list_favorite'),
    url(r'^work/comment/list/$', 'work_comment_list'),
    url(r'^work/comment/add/$', 'work_comment_add'),
    url(r'^work/comment/del/$', 'work_comment_del'),
    url(r'^work/rating/$', 'work_rating'),

    url(r'^chapter/list/$', 'chapter_list'),
    url(r'^chapter/view/$', 'chapter_view'),
    url(r'^chapter/comment/list/$', 'chapter_comment_list'),
    url(r'^chapter/comment/add/$', 'chapter_comment_add'),
    url(r'^chapter/comment/del/$', 'chapter_comment_del'),
    url(r'^chapter/rating/$', 'chapter_rating'),
    url(r'^chapter/rating/add/$', 'chapter_rating_add'),
)
