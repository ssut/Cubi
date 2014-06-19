# -*- encoding: utf-8 -*-
import json
import StringIO as oStringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from datetime import datetime
from textwrap import dedent as trim
from cStringIO import StringIO

from PIL import Image as PIL_Image

from author.forms import AddworkForm
from author.models import AuthorInfo
from work.models import *
from work.crawl import make_directory, save_chapter_contents
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

def update(request):
    if request.method == 'POST':
        author_info = AuthorInfo.objects.get(user=request.user)
        d = {
            'success': False,
            'message': '',
        }
        t = request.POST.get('type', '')

        if t == 'thumbnail':
            image = request.FILES.get('image', '')
            try:
                io = StringIO()
                for chunk in image.chunks():
                    io.write(chunk)
                io.seek(0)
                im = PIL_Image.open(io)
                im.thumbnail((64, 64), PIL_Image.ANTIALIAS)

                tmp = oStringIO.StringIO()
                im.save(tmp, 'JPEG')

                tmp_file = InMemoryUploadedFile(tmp, None, 'foo.jpg',
                                                'image/jpeg', tmp.len, None)
                author_info.profile_image = tmp_file
                author_info.save()
            except Exception, e:
                d['message'] = str(e)
            else:
                d['success'] = True
                d['message'] = author_info.profile_image.url
        elif t == 'description':
            val = request.POST.get('value', '')
            try:
                author_info.introduce_simple = val
                author_info.save()
            except Exception, e:
                d['message'] = str(e)
            else:
                d['success'] = True

        return HttpResponse(json.dumps(d), content_type='application/json')


# 작품 업로드 약관 동의
def agreement(request):
    if request.method == 'POST':  # 여기로 온 이상 무조건 동의한걸로 간주
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
        return render_to_response('author/agreement.html',
                                  RequestContext(request))

# 작품 업로드 메인
def index(request):
    user = request.user
    if user.type != '2':
        return redirect('author:agreement')
    else:
        author_info = AuthorInfo.objects.get(user=user)
        works = Work.objects.filter(author=user)
        d = {
            'author_info': author_info,
            'works': works,
        }
        return render_to_response('author/index.html', d,
                                  RequestContext(request))

'''
작품 업로드
    1. 타입 선택
    2. 정보 입력
'''
def addwork(request):
    if request.method == 'POST':
        name, desc = request.POST.get('name', ''), request.POST.get('desc', '')
        if name == '' or desc == '':
            d = {
                'success': False,
                'message': u'모든 폼을 채워주세요.'
            }
            return HttpResponse(json.dumps(d), content_type="application/json")

        if Work.objects.filter(title=name).exists():
            d = {
                'success': False,
                'message': u'이미 존재하는 작품명입니다.'
            }
            return HttpResponse(json.dumps(d), content_type="application/json")

        # Work Instance생성
        user = request.user
        category = WorkCategory.objects.get(title=u'웹툰')
        work_instance = Work(
            title=name,
            category=category,
            work_num=-1,
            description_simple=desc,
            author=user)
        work_instance.save()

        if work_instance:
            d = {
                'success': True
            }
            return HttpResponse(json.dumps(d), content_type="applicaiton/json")
    else:
        return render_to_response('author/add_work.html',
                                  RequestContext(request))

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
            return render_to_response('author/addwork_select_type_failed.html',
                                      d, RequestContext(request))
    else:
        return render_to_response('author/addwork_select_type.html',
                                  RequestContext(request))

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
            return render_to_response('author/addwork_info_failed.html', d,
                                      RequestContext(request))
    else:
        form = AddworkInfoForm()
        d = {'form': form}
        return render_to_response('author/addwork_info.html', d,
                                  RequestContext(request))

def editwork(request, work_id):
    work = Work.objects.get(id=work_id)

    if not work:
        return Http404()
    if request.method == 'POST':
        ref = request.META.get('HTTP_REFERER', '')
        try:
            t = request.POST.get('title', '')
            dl = request.POST.get('desc_lite', '')
            df = request.POST.get('desc_full', '')

            work.title = t if t else work.title
            work.description_simple = dl if dl else work.description_simple
            work.description_full = df if df else work.description_full

            def image_set(_name):
                if _name in request.FILES:
                    f = request.FILES[_name]
                    setattr(work, _name, f)

            image_set('image_thumbnail_square')
            image_set('image_thumbnail_rectangle')
            image_set('image_cover_large')
            image_set('image_cover')
            image_set('mobile_cover_top')
            image_set('mobile_cover_pager')
            image_set('mobile_cover_small')
            image_set('mobile_largeicon')
            image_set('mobile_smallicon')

            work.save()
        except Exception, e:
            html = """
            <script>
            alert("작품정보 수정 오류: {0}");
            history.go(-1);
            </script>
            """.format(e)
            return HttpResponse(html)
        else:
            html = """
            <script>
            alert("작품정보가 수정됐습니다.");
            location.replace("{0}");
            </script>
            """.format(ref)
            return HttpResponse(html)
    else:
        d = {
            'work': work
        }
        return render_to_response('author/edit_work.html', d,
                                  RequestContext(request))

def addchapter(request, work_id):
    work = Work.objects.get(id=work_id)

    if not work:
        return Http404()
    if request.method == 'POST':
        ref = request.POST.get('HTTP_REFERER', '')
        try:
            t = request.POST.get('title', '')
            d = request.POST.get('desc', '')

            if t == '' or d == '':
                raise ValueError(u'모든 폼을 채워주세요.')

            i = Chapter.objects.filter(work=work).count() + 1
            chapter = Chapter.objects.create(
                reg_no=i, work=work, title=t, description=d)

            images = []
            for filename, f in request.FILES.iteritems():
                if filename and f.name and f.name != '' and len(f) > 0:
                    io = StringIO()
                    io.write(f.read())
                    io.seek(0)

                images.append(io)

            make_directory()
            save_chapter_contents(chapter, work, images, None)
        except Exception, e:
            html = """
            <script>
            alert("작품정보 수정 오류: {0}");
            history.go(-1);
            </script>
            """.format(e)
            import traceback
            traceback.print_exc()
            return HttpResponse(html)
        else:
            html = """
            <script>
            alert("작품이 등록됐습니다.");
            location.replace("/chapter/list/{0}/");
            </script>
            """.format(work.id)
            return HttpResponse(html)
    else:
        d = {
            'work': work
        }
        return render_to_response('author/add_chapter.html', d,
                                  RequestContext(request))


'''
Author - ChapterList (작가의 작품목록에서 작품 클릭시 이쪽으로 넘어옴)
    작품의 모든 챕터 보여줌
    작품이 웹툰 자동 크롤링 상태일 때, reload버튼 필요
    특정 Chapter를 보이지 않도록 하는 옵션 필요 (visibility조절)
'''
def chapter_list(request):
    pass
