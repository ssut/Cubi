#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^django_admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # 1단계 메뉴
    url(r'^$', 'structure.views.index', name='index'),
    url(r'^about/$', 'structure.views.about', name='about'),

    # 공지사항
    url(r'^noticelist/$', 'board.views.noticelist', name='noticelist'),

    # 작품등록
    url(r'^reg_author/$', 'structure.views.reg_author', name='reg_author'),
    url(r'^reg_work/$', 'structure.views.reg_work', name='reg_work'),

    # 모바일
    url(r'^mobile/login/$', 'member.api.login', name='mobile_login'),
    url(r'^mobile/list/(\d+)/$', 'work.api.list', name='mobile_list'),
    url(r'^mobile/detail/(\d+)/(\d+)/$', 'work.api.detail', name='mobile_detail'),
    url(r'^mobile/chapter/commentrating/$', 'work.api.chapter_commentrating', name='mobile_chapter_commentrating'),
    url(r'^mobile/chapter/comment/add/$', 'work.api.chapter_comment_add', name='mobile_chapter_comment_add'),



    url(r'^worklist/$', 'structure.views.work_list', name='work_list'),
)
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))