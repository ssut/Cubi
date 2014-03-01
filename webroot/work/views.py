from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from cubi.functions import day_to_string
from cubi.settings import MEDIA_URL
from work.models import *


def work_list(request):
    query_dict = request.GET

    works = Work.objects.all().order_by('-created')
    work_dict_list = []
    for work in works:
        work_dict = work.json()
        chapters = Chapter.objects.filter(work=work).order_by('-created')
        chapter_count = chapters.count()
        last_chapter = chapters.last()
        work_dict['chapter_count'] = chapter_count
        work_dict['last_upload'] = day_to_string(last_chapter.created)
        work_dict_list.append(work_dict)
    
    d = {
        'media_url': MEDIA_URL,
        'works': work_dict_list,
    }

    return render_to_response('work/work_list.html', d, RequestContext(request))

def chapter_list(request, work_id):
    work = Work.objects.get(id=work_id)
    chapters = Chapter.objects.filter(work=work).order_by('-created')
    last_chapter = chapters.last()

    work_dict = work.json()
    work_dict['chapter_count'] = chapters.count()
    work_dict['last_upload'] = day_to_string(last_chapter.created)

    d = {
        'work': work_dict,
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