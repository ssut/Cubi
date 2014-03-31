#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template import RequestContext

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
    return render_to_response('temp/work_list.html', d, RequestContext(request))