#-*- encoding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from datetime import datetime
from textwrap import dedent as trim

from author.forms import AddworkForm
from author.models import AuthorInfo
from work.models import *
from member.models import TinicubeUser as User

REAL_PATH = ''
FIELD_PATH = ''
MEDIA_PATH = settings.MEDIA_ROOT

# 작품 업로드 소개
def introduce(request):
    return render_to_response('author/introduce.html', RequestContext(request))

def info(request, author_id):
    author = User.objects.get(id=author_id)
    if not author or author.type != '2':
        return HttpResponse(trim("""\
            <script>
            alert("존재하지 않는 회원이거나 작가가 아닙니다.");
            history.go(-1);
            </script>
        """))
    else:
        author_info = AuthorInfo.objects.get(user=author)
        works = Work.objects.filter(author=author)
        d = {
            'author': author,
            'author_info': author_info,
            'works': works,
        }
        return render_to_response('author/info.html', d)

# 작품 업로드 약관 동의
def agreement(request):
    if request.method == 'POST': # 여기로 온 이상 무조건 동의한걸로 간주
        query_dict = request.POST
        # 업로드 동의 시, 유저 타입을 2(작가)로 변경함
        user = request.user
        user.type = '2'
        user.save()

        # 동시에 AuthorInfo인스턴스 만들어 배정
        authorinfo_instance = AuthorInfo(user=user, nickname=user.nickname)
        authorinfo_instance.save()

        return redirect('author:index')
    else:
        return render_to_response('author/agreement.html', RequestContext(request))

# 작품 업로드 메인
def index(request):
    user = request.user
    if user.type != '2':
        return redirect('author:introduce')
    else:
        author_info = AuthorInfo.objects.get(user=user)
        works = Work.objects.filter(author=user)
        d = {
            'author_info': author_info,
            'works': works,
        }
        return render_to_response('author/index.html', d, RequestContext(request))

'''
작품 업로드
    1. 타입 선택
    2. 정보 입력
'''
def addwork(request):
    if request.method == 'POST':
        form = AddworkForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            type = form.cleaned_data['type']
            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']
            introduce = form.cleaned_data['introduce']
            work_num = form.cleaned_data['work_num']
            image_cover = form.cleaned_data['image_cover']
            image_thumbnail = form.cleaned_data['image_thumbnail']
            image_loading = form.cleaned_data['image_loading']
            image_largeicon = form.cleaned_data['image_largeicon']
            image_smallicon = form.cleaned_data['image_smallicon']

            # print dir(image_cover.file)
            name, ext = os.path.splitext(image_cover.name)
            print name
            print ext

            if type == 'webtoon_naver':
                work_category = WorkCategory.objects.get(title=u'웹툰')
            elif type == 'webtoon_daum':
                work_category = WorkCategory.objects.get(title=u'웹툰')
            
            # Work Instance생성
            user = request.user
            work_instance = Work(category=work_category, author=user, title=title, 
                description=introduce, work_num=work_num)
            work_instance.save()

            # 이미지파일 저장
            # today = datetime.today()
            # today_str = today.strftime('%Y%m%d')
            # REAL_PATH = os.path.join(MEDIA_PATH, today_str, 'work', 'webtoon')
            # FIELD_PATH = os.path.join(today_str, 'work', 'webtoon')

            # print 'REAL_PATH :', REAL_PATH
            # if not os.path.exists(REAL_PATH):
            #     os.makedirs(REAL_PATH)
            #     print 'real path created'

            # cover_filename = u'%s_cover%s' % (work_instance.id, ext)
            # thumbnail_filename = u'%s_thumbnail%s' % (work_instance.id, ext)
            # loading_filename = u'%s_loading%s' % (work_instance.id, ext)
            # largeicon_filename = u'%s_largeicon%s' % (work_instance.id, ext)
            # smallicon_filename = u'%s_smallicon%s' % (work_instance.id, ext)

            # cover_realpath = os.path.join(REAL_PATH, cover_filename)
            # cover_fieldpath = os.path.join(FIELD_PATH, cover_filename)
            # thumbnail_realpath = os.path.join(REAL_PATH, thumbnail_filename)
            # thumbnail_fieldpath = os.path.join(FIELD_PATH, thumbnail_filename)
            # loading_realpath = os.path.join(REAL_PATH, loading_filename)
            # loading_fieldpath = os.path.join(FIELD_PATH, loading_filename)
            # largeicon_realpath = os.path.join(REAL_PATH, largeicon_filename)
            # largeicon_fieldpath = os.path.join(FIELD_PATH, largeicon_filename)
            # smallicon_realpath = os.path.join(REAL_PATH, smallicon_filename)
            # smallicon_fieldpath = os.path.join(FIELD_PATH, smallicon_filename)            
            
            # Work 인스턴스에 이미지 저장
            work_instance.cover = image_cover
            work_instance.image_loading = image_loading
            work_instance.image_largeicon = image_largeicon
            work_instance.image_smallicon = image_smallicon
            work_instance.save()

            d = {
                'title': title,
            }

            return render_to_response('author/addwork_success.html', d, RequestContext(request))

        else:
            error_msg = u'업로드 데이터가 잘못되었습니다'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('author/addwork_failed.html', d, RequestContext(request))
    else:
        form = AddworkForm()
        d = {'form': form}
        return render_to_response('author/addwork.html', d, RequestContext(request))

# 작품 업로드 1 - 타입 선택 (웹툰, 만화, 소설 등)
def addwork_select_type(request):
    if request.method == 'POST':
        query_dict = request.POST
        print query_dict
        type_value = query_dict.get('type', '')
        if type_value == 'webtoon_naver':
            return redirect('author:addwork_info')
        elif type_value == 'webtoon_daum':
            return redirect('author:addwork_info')
        else:
            error_msg = u'타입을 선택해주세요'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('author/addwork_select_type_failed.html', d, RequestContext(request))
    else:
        return render_to_response('author/addwork_select_type.html', RequestContext(request))

# 작품 업로드 2 - 해당 정보 입력
def addwork_info(request):
    if request.method == 'POST':
        form = AddworkInfoForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            print form.cleaned_data
            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']
            introduce = form.cleaned_data['introduce']
            work_num = form.cleaned_data['work_num']
            image_cover = form.cleaned_data['image_cover']
            image_thumbnail = form.cleaned_data['image_thumbnail']
            image_loading = form.cleaned_data['image_loading']
            image_largeicon = form.cleaned_data['image_largeicon']
            image_smallicon = form.cleaned_data['image_smallicon']

            


        else:
            error_msg = u'업로드 데이터가 잘못되었습니다'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('author/addwork_info_failed.html', d, RequestContext(request))
    else:
        form = AddworkInfoForm()
        d = {'form': form}
        return render_to_response('author/addwork_info.html', d, RequestContext(request))

'''
Author - ChapterList (작가의 작품목록에서 작품 클릭시 이쪽으로 넘어옴)
    작품의 모든 챕터 보여줌
    작품이 웹툰 자동 크롤링 상태일 때, reload버튼 필요
    특정 Chapter를 보이지 않도록 하는 옵션 필요 (visibility조절)
'''
def chapter_list(request):
    pass