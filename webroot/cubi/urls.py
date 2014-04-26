#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^django_admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^$', 'structure.views.index', name='index'),

    # 작품 목록
    url(r'^work/list/$', 'work.views.work_list', name='work_list'),
    # 챕터 목록
    url(r'^chapter/list/(\d+)/$', 'work.views.chapter_list', name='chapter_list'),
    # 챕터 뷰
    url(r'^chapter/view/(\d+)/$', 'work.views.chapter_view', name='chapter_view'),

    ## Member
    # 로그인
    url(r'^signin/$', 'member.views.signin', name='signin'),
    # 회원 가입
    url(r'^signup/$', 'member.views.signup', name='signup'),
    # 로그아웃
    url(r'^signout/$', 'member.views.signout', name='signout'),
    # 작가전환
    url(r'^convert/$', 'member.views.convert_to_author', name='convert_to_author'),
    # 회원 정보
    url(r'^member/info/$', 'member.views.member_info', name='member_info'),
    # 비밀번호 변경
    url(r'^member/passwordchange/$', 'member.views.password_change', name='password_change'),

    # Author(나의 작품)
    url(r'^author/', include('author.urls', namespace='author')),

    ## Administrator
    url(r'^admin/', include('administrator.urls', namespace='administrator')),



    # 공지사항
    url(r'^notice/list/$', 'board.views.notice_list', name='notice_list'),
    url(r'^notice/view/(\d+)/$', 'board.views.notice_view', name='notice_view'),

    # 작품등록
    url(r'^reg_author/$', 'structure.views.reg_author', name='reg_author'),
    url(r'^reg_work/$', 'structure.views.reg_work', name='reg_work'),

    # API
    url(r'^api/', include('cubi.urls_api')),
    


    url(r'^worklist/$', 'structure.views.work_list', name='work_list_api'),
)
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))