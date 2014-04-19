#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q

from cubi.functions import day_to_string
from cubi.settings import MEDIA_URL

from django.core.paginator import Paginator

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from author.models import WaitConvert
from work.models import *

import json

def index(request):
    return render_to_response('administrator/index.html', RequestContext(request))

def wait_convert_list(request):
    waiting_list = WaitConvert.objects.all().order_by('-created')
    d = {
        'waiting_list': waiting_list,
    }
    return render_to_response('administrator/wait_convert_list.html', d, RequestContext(request))

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
            return render_to_response('administrator/convert_success.html', d, RequestContext(request))
        except:
            d = {'reason': u'작가 전환 실패'}
            return render_to_response('administrator/convert_failed.html', d, RequestContext(request))
    else:
        d = {'reason': u'작가 전환 실패'}
        return render_to_response('administrator/convert_failed.html', d, RequestContext(request))


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

    return render_to_response('administrator/work_list.html', d, RequestContext(request))

def crawl_list(request):
    d = {
        'targets': ChapterQueue.TARGET_CHOICES,
    }

    return render_to_response('administrator/crawl_list.html', d, RequestContext(request))

def add_crawl_list(request):
    if not request.method == 'POST' or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    d = {
        'success': False,
        'message': ''
    }

    target = request.POST.get('target', None)
    comic_number = int(request.POST.get('comic_number', '0'))
    time = int(request.POST.get('time', '0'))
    user = int(request.POST.get('user', '0'))

    l = [item[0] for item in ChapterQueue.TARGET_CHOICES]
    # if not target in l:
        




def search_user(request):
    keyword = request.GET.get('query', None).replace('@', '')
    if keyword is None or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    user_list = User.objects.filter(Q(username__contains=keyword) |
                                    Q(nickname__contains=keyword) |
                                    Q(email__contains=keyword))

    d = {
        'query': keyword,
        'suggestions': [],
    }
    for user in user_list:
        d['suggestions'].append({
                'value': '{0} ({1})'.format(user.username, user.email),
                'data': user.id,
            })

    return HttpResponse(json.dumps(d), content_type="application/json")


