# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template import RequestContext

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from work.models import *
from board.models import Notice


def temp(request):
    return render_to_response('index/temp.html')

def index(request):
    recent_works = Work.objects.all().order_by('-created')[:5]
    recent_notices = Notice.objects.all().order_by('-created')[:10]

    d = {
        'works': recent_works,
        'notices': recent_notices,
    }
    return render_to_response('index/index.html', d, RequestContext(request))

def about(request):
    return render_to_response('about.html')

def reg_author(request):
    return render_to_response('reg_author.html')

def reg_work(request):
    return render_to_response('reg_work.html')

def work_list(request):
    works = Work.objects.all().order_by('-created')
    d = {
        'works': works,
    }
    return render_to_response('work/work_list.html', d,
                              RequestContext(request))

def author_list(request):
    authors = User.objects.filter(type='2')
    d = {
        'authors': authors,
    }
    return render_to_response('index/author_list.html', d,
                              RequestContext(request))

def terms(request):
    return render_to_response('terms.html')

def privacy(request):
    return render_to_response('privacy.html')

def error(request):
    return render_to_response('error.html')
