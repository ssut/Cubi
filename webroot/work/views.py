#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from cubi.functions import day_to_string
from cubi.settings import MEDIA_URL
from work.models import *

'''
작품목록
    /work/list/
    모든 작품(work) 목록 표시
    각 작품에 chapter_count와 last_upload를 넣어서 반환
'''
def work_list(request):
    works = Work.objects.all().order_by('-created')    
    d = {
        'media_url': MEDIA_URL,
        'works': works,
    }

    return render_to_response('work/work_list.html', d, RequestContext(request))

def chapter_list(request, work_id):
    work = Work.objects.get(id=work_id)
    chapters = Chapter.objects.filter(work=work).order_by('-created')

    d = {
        'work': work,
        'chapters': chapters,
    }

    return render_to_response('work/chapter_list.html', d, RequestContext(request))

def chapter_view(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    images = Image.objects.filter(chapter=chapter)

    d = {
        'images': images,
        'media_url': MEDIA_URL,
    }

    return render_to_response('work/chapter_view.html', d, RequestContext(request))