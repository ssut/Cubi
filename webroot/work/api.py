#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

import json

from cubi.settings import MEDIA_URL
from work.models import *

def list(request, work_id):
    work = Work.objects.get(id=work_id)
    chapters = Chapter.objects.filter(work=work).order_by('-created')

    chapter_info_list = []
    for chapter in chapters:
        chapter_dict = chapter.json()
        ratings = ChapterRating.objects.filter(chapter=chapter)
        if ratings:
            total_rating = 0.0
            for rating in ratings:
                total_rating = total_rating + rating.score
            avg_rating = total_rating / len(ratings)
            chapter_dict['rating'] = avg_rating
            chapter_dict['rating_number'] = len(ratings)
            chapter_info_list.append(chapter_dict)
        else:
            chapter_dict['rating'] = 0.0
            chapter_dict['rating_number'] = 0
            chapter_info_list.append(chapter_dict)

    data = {
        'work': work.json(),
        # 'chapters': [chapter.json() for chapter in chapters],
        'chapters': chapter_info_list,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")

def detail(request, work_id, chapter_id):
    work = Work.objects.get(id=work_id)
    chapter = Chapter.objects.get(work=work, id=chapter_id)
    images = Image.objects.filter(chapter=chapter)
    print images
    contents = Content.objects.filter(chapter=chapter)
    print contents

    d = {
        'images': images,
        'media_url': MEDIA_URL,
    }

    return render_to_response('mobile/chapter.html', d)