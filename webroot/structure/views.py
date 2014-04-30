#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template import RequestContext

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


from work.models import *

def index(request):
    return render_to_response('index/index.html', RequestContext(request))

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
    return render_to_response('work/work_list.html', d, RequestContext(request))

def author_list(request):
    authors = User.objects.filter(type='2')
    d = {
        'authors': authors,
    }
    return render_to_response('index/author_list.html', d, RequestContext(request))