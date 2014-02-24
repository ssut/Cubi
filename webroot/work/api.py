#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.db.models import Avg

# decorator
from django.views.decorators.csrf import csrf_exempt

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

import json

from cubi.settings import MEDIA_URL
from cubi.functions import return_failed_json, return_success_json
from work.models import *



'''
Work
'''


'''
Chapter
    chapter_list : 댓글 목록
    chapter_view : 해당 chapter의 webview화면
    chapter_comment_list : 댓글 목록
    chapter_commnet_add : 댓글 추가
    chapter_comment_del : 댓글 삭제
    chapter_rating : 평점
    chapter_rating_add : 평점 추가
'''
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

            # 평점 분석
            ratings = ChapterRating.objects.filter(chapter=chapter)
            avg_rating = ratings.aggregate(Avg('score'))['score__avg']
            if avg_rating:
                chapter_dict['rating'] = avg_rating
                chapter_dict['rating_number'] = ratings.count()
                chapter_info_list.append(chapter_dict)
            else:
                chapter_dict['rating'] = 0.0
                chapter_dict['rating_number'] = 0
                chapter_info_list.append(chapter_dict)

        data = {
            'work': work.json(),
            'chapters': chapter_info_list,
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return return_failed_json('Must POST Request')

@csrf_exempt
def chapter_view(request):
    if request.method == 'POST':
        query_dict = request.POST
        work_id = int(query_dict['work_id'])
        chapter_id = int(query_dict['chapter_id'])

        work = Work.objects.get(id=work_id)
        chapter = Chapter.objects.get(work=work, id=chapter_id)
        images = Image.objects.filter(chapter=chapter)
        contents = Content.objects.filter(chapter=chapter)

        d = {
            'images': images,
            'media_url': MEDIA_URL,
        }

        return render_to_response('mobile/chapter.html', d)
    else:
        return return_failed_json('Must POST Request')

# 댓글 목록
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

# 댓글 추가
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

# 댓글 삭제
@csrf_exempt
def chapter_comment_del(request):
    if request.method == 'POST':
        query_dict = request.POST
        session_key = query_dict['session_key']
        username = query_dict['username']
        work_id = int(query_dict['work_id'])
        chapter_id = int(query_dict['chapter_id'])
        comment_id = int(query_dict['comment_id'])

        s = SessionStore(session_key=session_key)

        if username == s['username']:
            user = User.objects.get(username=s['username'])
            work = Work.objects.get(id=work_id)
            chapter = Chapter.objects.get(work=work, id=chapter_id)
            comment = ChapterComment.objects.get(id=comment_id)

            # 댓글 작성자와 사용자가 같을 경우 댓글 삭제
            if comment.author == user:
                comment.delete()
                return return_success_json()
            else:
                return return_failed_json('request user is not comment\'s author')
            
        else:
            return return_failed_json('Not Matching User')

    else:
        return return_failed_json('Must POST Request')

@csrf_exempt
def chapter_rating(request):
    if request.method == 'POST':
        query_dict = request.POST
        work_id = int(query_dict['work_id'])
        chapter_id = int(query_dict['chapter_id'])

        chapter = Chapter.objects.get(id=chapter_id)
        dict = {}

        # 평점 분석
        ratings = ChapterRating.objects.filter(chapter=chapter)
        avg_rating = ratings.aggregate(Avg('score'))['score__avg']
        if avg_rating:
            dict['rating'] = avg_rating
            dict['rating_number'] = ratings.count()
        else:
            dict['rating'] = 0.0
            dict['rating_number'] = 0

        return HttpResponse(json.dumps(dict), content_type='application/json')
    else:
        return return_failed_json('Must POST Request')

@csrf_exempt
def chapter_rating_add(request):
    if request.method == 'POST':
        query_dict = request.POST
        session_key = query_dict['session_key']
        username = query_dict['username']
        work_id = int(query_dict['work_id'])
        chapter_id = int(query_dict['chapter_id'])
        rating = int(query_dict['rating'])

        s = SessionStore(session_key=session_key)

        if username == s['username']:
            user = User.objects.get(username=s['username'])
            work = Work.objects.get(id=work_id)
            chapter = Chapter.objects.get(work=work, id=chapter_id)

            if ChapterRating.objects.filter(chapter=chapter).filter(author=user).exists():
                rating_instance = ChapterRating.objects.get(chapter=chapter, author=user)
                rating_instance.score = rating
                rating_instance.save()
            else:
                rating_instance = ChapterRating.objects.create(chapter=chapter, author=user, score=rating)
                rating_instance.save()
            return return_success_json()
        else:
            return return_failed_json('Not Matching User')

    else:
        return return_failed_json('Must POST Request')