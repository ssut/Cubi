#-*- coding: utf-8 -*-
import json

from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from tinicube.functions import day_to_string
from tinicube.settings import MEDIA_URL
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
    user = request.user

    rating = chapter.avg_rating['rating'] if 'rating' in chapter.avg_rating else '0'
    d = {
        'chapter': chapter,
        'images': images,
        'media_url': MEDIA_URL,
        'avg_rating': rating,
        'user_rated': False,
        'comments': ChapterComment.objects.filter(chapter=chapter).order_by('-created')
    }

    if user.is_authenticated:
        rating = ChapterRating.objects.filter(chapter=chapter, author=user).exists()
        if rating:
            print rating
            d['user_rated'] = True

    return render_to_response('work/chapter_view.html', d, RequestContext(request))

def add_chapter_rating(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    user = request.user

    if chapter and not ChapterRating.objects.filter(chapter=chapter, author=user).exists():
        rating = ChapterRating.objects.create(
            author=user,
            score=int(request.POST.get('rating', '')),
            chapter=chapter
        )
        url = reverse('chapter_view', chapter.id)
        return HttpResponse('<script> location.replace("' + url + '") </script>')

def add_chapter_comment(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    user = request.user
    comment = request.POST.get('comment', '')

    if chapter and len(comment) > 0:
        comment = ChapterComment.objects.create(
            author=user,
            content=comment,
            chapter=chapter
        )
        url = '/chapter/view/' + str(chapter.id)
        return HttpResponse('<script> location.replace("' + url + '") </script>')

def update_chapter(request):
    if request.method == 'POST':
        t = request.POST.get('type', '')
        i = request.POST.get('id', '')
        chapter = Chapter.objects.get(id=i)
        if not chapter:
            return
        work = chapter.work

        if t == 'update':
            d = {}
            queue = ChapterQueue.objects.filter(target=work.work_target,
                comic_number=work.work_num,
                chapter_number=chapter.reg_no,
                is_checked=False)
            if queue:
                d['success'] = False
                d['message'] = u'이미 등록된 큐가 있습니다.'
            else:
                queue = ChapterQueue.objects.create(
                    target=work.work_target,
                    user=request.user,
                    comic_number=work.work_num,
                    chapter_number=chapter.reg_no,
                    checked_at=datetime.now()
                    )
                d['success'] = True
                d['message'] = u'큐에 등록되었습니다.'

            return HttpResponse(json.dumps(d), content_type='application/json')
        elif t == 'public':
            chapter.public = not chapter.public
            chapter.save()
            d = {
                'message': (u'공개 설정되었습니다.' if chapter.public else u'비공개 설정되었습니다.'),
                'public': chapter.public,
            }
            return HttpResponse(json.dumps(d), content_type='application/json')



