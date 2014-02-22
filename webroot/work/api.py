#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

# decorator
from django.views.decorators.csrf import csrf_exempt

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

import json

from cubi.settings import MEDIA_URL
from cubi.functions import return_failed_json, return_success_json
from work.models import *


@csrf_exempt
def chapter_list(request):
    if request.method == 'POST':
        query_dict = request.POST
        work_id = int(query_dict['work_id'])
        work = Work.objects.get(id=work_id)
        chapters = Chapter.objects.filter(work=work).order_by('-created')

        chapter_info_list = []
        for chapter in chapters:
            chapter_dict = chapter.json()

            # 평점 분석. 너무 비효율적인 것 같음
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
    else:
        return return_failed_json('Must POST Request')

@csrf_exempt
def chapter_view(request, work_id, chapter_id):
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

'''
Chapter - 댓글(Comment), 평점(Rating)
'''
@csrf_exempt
def chapter_comment_list(request):
    if request.method == 'POST':
        query_dict = request.POST
        work_id = int(query_dict['work_id'])
        chapter_id = int(query_dict['chapter_id'])

        comments = ChapterComment.objects.filter(chapter__id=chapter_id).filter(chapter__work__id=work_id)

        data = {
            'comments': [comment.json() for comment in comments],
        }

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return return_failed_json('Must POST Request')

@csrf_exempt
def chapter_comment_add(request):
    if request.method == 'POST':
        query_dict = request.POST
        session_key = query_dict['session_key']
        username = query_dict['username']
        work_id = int(query_dict['work_id'])
        chapter_id = int(query_dict['chapter_id'])
        content = query_dict['content']

        s = SessionStore(session_key=session_key)

        # 유저가 세션값의 유저와 같으면 글 등록
        if username == s['username']:
            user = User.objects.get(username=s['username'])
            work = Work.objects.get(id=work_id)
            chapter = Chapter.objects.get(work=work, id=chapter_id)

            comment_instance = ChapterComment(chapter=chapter, author=user, content=content)
            comment_instance.save()
            return return_success_json()
        else:
            return return_failed_json('Not Matching User')

    else:
        return return_failed_json('Must POST Request')