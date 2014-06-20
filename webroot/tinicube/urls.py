# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

handler404 = 'structure.views.error'
urlpatterns = patterns(
    '',

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^django_admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^$', 'structure.views.index', name='index'),
    # url(r'^$', 'structure.views.temp', name='temp'),

    url(r'^terms/$', 'structure.views.terms', name='terms'),
    url(r'^privacy/$', 'structure.views.privacy', name='privacy'),

    # 작품 목록
    url(r'^work/list/$', 'work.views.work_list', name='work_list'),
    # 챕터 목록
    url(r'^chapter/list/(\d+)/$', 'work.views.chapter_list',
        name='chapter_list'),
    # 챕터 뷰
    url(r'^chapter/view/(\d+)/$', 'work.views.chapter_view',
        name='chapter_view'),

    # 댓글 쓰기
    url(r'^chapter/(\d+)/comment$', 'work.views.add_chapter_comment',
        name='add_chapter_comment'),

    # 평점 보내기
    url(r'^chapter/(\d+)/rating$', 'work.views.add_chapter_rating',
        name='add_chapter_rating'),

    # (작가 전용) 작품 업데이트 (공개설정 변경, 갱신)
    url(r'^chapter/update$', 'work.views.update_chapter',
        name='update_chapter'),

    # 작가 목록
    url(r'^author/list/$', 'structure.views.author_list',
        name='author_list'),

    # 로그인
    url(r'^signin/$', 'member.views.signin', name='signin'),
    # 회원 가입
    url(r'^signup/$', 'member.views.signup', name='signup'),
    # 로그아웃
    url(r'^signout/$', 'member.views.signout', name='signout'),
    # 작가전환
    url(r'^convert/$', 'member.views.convert_to_author',
        name='convert_to_author'),
    # 회원 정보
    url(r'^member/info/$', 'member.views.member_info',
        name='member_info'),
    # 비밀번호 변경
    url(r'^member/passwordchange/$', 'member.views.password_change',
        name='password_change'),

    # Author(나의 작품)
    url(r'^author/', include('author.urls', namespace='author')),

    # Administrator
    url(r'^admin/', include('administrator.urls', namespace='administrator')),

    # Users
    url(r'^user/', include('member.urls', namespace='member')),
    url(r'auth/', include('social_auth.urls')),


    # 공지사항
    url(r'^notice/list/$', 'board.views.notice_list',
        name='notice_list'),
    url(r'^notice/view/(\d+)/$', 'board.views.notice_view',
        name='notice_view'),

    # 작품등록
    url(r'^reg_author/$', 'structure.views.reg_author', name='reg_author'),
    url(r'^reg_work/$', 'structure.views.reg_work', name='reg_work'),

    # API
    url(r'^api/', include('tinicube.urls_api')),


    url(r'^worklist/$', 'structure.views.work_list', name='work_list_api'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (
            r'^media/(?P<path>.*)$',
            'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT
            }
        )
    )
