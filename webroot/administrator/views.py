# -*- coding: utf-8 -*-
import json

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from tinicube.functions import day_to_string
from tinicube.settings import MEDIA_URL

from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from work import crawl as crawler
from work.models import *

from crawler import daum_leaguetoon as DaumLeaguetoon
from crawler.exceptions import WebtoonDoesNotExist, WebtoonChapterDoesNotExist
from crawler.naver_webtoon import NaverWebtoon

from datetime import datetime


def index(request):
    return render_to_response('administrator/index.html',
                              RequestContext(request))



def convert(request, user_id, boolean):
    user = User.objects.get(id=user_id)
    if WaitConvert.objects.filter(user=user).exists():
        waitconvert = WaitConvert.objects.get(user=user)
        try:
            if boolean == 'true':
                user.type = '2'
                d = {'reason': u'작가 전환 성공'}
            elif boolean == 'false':
                user.type == '1'
                d = {'reason': u'작가 전환 실패'}
            user.save()
            waitconvert.delete()
            return render_to_response('administrator/convert_success.html', d,
                                      RequestContext(request))
        except:
            d = {'reason': u'작가 전환 실패'}
            return render_to_response('administrator/convert_failed.html', d,
                                      RequestContext(request))
    else:
        d = {'reason': u'작가 전환 실패'}
        return render_to_response('administrator/convert_failed.html', d,
                                  RequestContext(request))


def member_list(request, type='1'):
    if type == 'author':
        members = User.objects.filter(type='2')
        template = 'administrator/author_list.html'
    else:
        members = User.objects.filter(type='1')
        template = 'administrator/member_list.html'

    d = {
        'members': members,
        'media_url': MEDIA_URL,
    }

    return render_to_response(template, d, RequestContext(request))


def work_list(request):
    # if request.method == 'POST':
    #     query_dict = request.POST
    works = Work.objects.all().order_by('-created')
    d = {
        'works': works,
        'media_url': MEDIA_URL,
    }

    return render_to_response('administrator/work_list.html', d,
                              RequestContext(request))


def crawl_list(request):
    d = {
        'targets': ChapterQueue.TARGET_CHOICES,
    }

    return render_to_response('administrator/crawl_list.html', d,
                              RequestContext(request))


def get_crawl_list(request):
    num = int(request.GET.get('no', '0'))
    if num is 0 or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    crawl_list = ChapterPeriodicQueue.objects.all()
    paginator = Paginator(crawl_list, 25)

    try:
        items = paginator.page(num)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    # import pdb; pdb.set_trace()
    d = {
        'items': [{
            'id': x.id,
            'target': x.target,
            'user': str(x.user),
            'comic_number': x.comic_number,
            'every_hour': x.every_hour,
            'last_run_at': str(x.last_run_at),
            'last_run_result': x.last_run_result,
            'enabled': x.enabled,
        } for x in items.object_list],
        'current_page': num,
        'num_pages': paginator.num_pages,
    }
    return HttpResponse(json.dumps(d, cls=DjangoJSONEncoder),
                        content_type="application/json")


def add_crawl_list(request):
    if not request.method == 'POST' or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    d = {
        'success': False,
        'message': ''
    }

    target = request.POST.get('target', None)
    num = int(request.POST.get('comic_number', '0'))
    time = int(request.POST.get('time', '0'))
    user = int(request.POST.get('user', '0'))

    l = [item[0] for item in ChapterQueue.TARGET_CHOICES]
    if target not in l:
        d['message'] = 'target error'
    elif ChapterPeriodicQueue.objects.filter(comic_number=num).count() > 0:
        d['message'] = 'comic number already exists'
    elif time > 23 or time < 0:
        d['message'] = 'time error'
    elif not User.objects.filter(id=user).exists():
        d['message'] = 'user not exists'
    else:
        method = NaverWebtoon(
        ).list if target == ChapterQueue.NAVER else DaumLeaguetoon.list
        try:
            method(num)
        except Exception, e:
            d['message'] = 'webtoon not exists'
        else:
            queue = ChapterPeriodicQueue.objects.create(
                target=target,
                user=User.objects.get(id=user),
                comic_number=num,
                every_hour=time,
                last_run_at=datetime.now(),
                last_run_result=False
            )
            queue.save()
            d['success'] = True

    return HttpResponse(json.dumps(d), content_type="application/json")


def crawl_instantly(request):
    if not request.method == 'POST' or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    d = {
        'success': False,
        'message': ''
    }

    target = request.POST.get('target', None)
    comic_number = int(request.POST.get('comic_number', '0'))
    chapter_number = int(request.POST.get('chapter_number', '0'))
    user = int(request.POST.get('user', '0'))

    l = [item[0] for item in ChapterQueue.TARGET_CHOICES]
    if target not in l:
        d['message'] = 'target error'
    elif not User.objects.filter(id=user).exists():
        d['message'] = 'user not exists'
    else:
        method = NaverWebtoon(
        ).detail if target == ChapterQueue.NAVER else DaumLeaguetoon.detail
        try:
            method(comic_number, chapter_number)
        except WebtoonDoesNotExist, e:
            d['message'] = 'webtoon not exists'
        except WebtoonChapterDoesNotExist, e:
            d['message'] = 'webtoon chapter not exists'
        else:
            result = crawler.crawl(type=target, comic_number=comic_number,
                                   chapter_number=chapter_number,
                                   user=User.objects.get(id=user))
            if result is True:
                d['success'] = True
            else:
                d['message'] = 'webtoon crawling failed'

    return HttpResponse(json.dumps(d), content_type="applcation/json")


def toggle_crawl_enabled(request):
    _id = request.POST.get('id', None)
    _enabled = True if request.POST.get('enabled', 'off') == 'on' else False
    if _id is None or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    d = {
        'success': False
    }

    obj = ChapterPeriodicQueue.objects.get(id=_id)
    if obj is not None:
        d['success'] = True
        obj.enabled = _enabled
        obj.save()

    return HttpResponse(json.dumps(d), content_type="application/json")


def search_user(request):
    keyword = request.GET.get('query', None).replace('@', '')
    if keyword is None or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    user_list = User.objects.filter(Q(username__contains=keyword) |
                                    Q(first_name__contains=keyword) |
                                    Q(nickname__contains=keyword) |
                                    Q(email__contains=keyword))

    d = {
        'query': keyword,
        'suggestions': [],
    }
    for user in user_list:
        d['suggestions'].append({
            'value': u'{0} ({2}{3}, {1})'.format(user.username, user.email,
                                                 user.last_name,
                                                 user.first_name),
            'data': user.id,
        })

    return HttpResponse(json.dumps(d), content_type="application/json")
