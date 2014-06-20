# -*- coding: utf-8 -*-
import json

from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# exceptions
from django.core.exceptions import ObjectDoesNotExist

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from tinicube.functions import return_failed_json, return_success_json
from tinicube.settings import MEDIA_URL

from work.models import *


'''
통합 앱 용 API
    recent_update_chapter_list : 최근 업데이트 Chapter 목록
    new_work_list : 신규 Work 목록
    popular_work_list : 인기 Work 목록
    new_author_list : 신규 Author 목록
    popular_author_list : 인기 Author 목록

    all_work_list : 모든 Work 목록
'''
# 최근 업데이트 Chapter 목록
@require_http_methods(["POST"])
@csrf_exempt
def recent_update_chapter_list(request):
    chapters = Chapter.objects.all().order_by('-created')[:5]
    data = {
        'chapters': [chapter.json() for chapter in chapters]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

# 신규 Work 목록
@require_http_methods(["POST"])
@csrf_exempt
def new_work_list(request):
    works = Work.objects.all().order_by('-created')[:3]
    data = {
        'works': [work.json() for work in works]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

# 인기 Work 목록
@require_http_methods(["POST"])
@csrf_exempt
def popular_work_list(request):
    works = Work.objects.all().order_by('-created')[:5]
    data = {
        'works': [work.json() for work in works]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

# 신규 Author 목록
@require_http_methods(["POST"])
@csrf_exempt
def new_author_list(request):
    authors = User.objects.filter(type='2').filter(is_superuser=False).order_by('date_joined')[:3]
    data = {
        'authors': [author.json() for author in authors]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

# 인기 Author 목록
@require_http_methods(["POST"])
@csrf_exempt
def popular_author_list(request):
    authors = User.objects.filter(type='2').filter(is_superuser=False).order_by('date_joined')[:5]
    data = {
        'authors': [author.json() for author in authors]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

# 모든 Work 목록
@require_http_methods(["POST"])
@csrf_exempt
def all_work_list(request):
    works = Work.objects.all().order_by('-created')
    data = {
        'works': [work.json() for work in works]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
'''
Work
    work_list : Work 목록
    work_list_favorite : 즐겨찾는 Work 목록
    work_comment_list : 댓글 목록
    work_comment_add : 댓글 추가
    work_comment_del : 댓글 삭제
    work_rating : 평점
        모든 Chapter의 평점 평균으로 계산
'''
# 작품 목록
@require_http_methods(["POST"])
@csrf_exempt
def work_list(request):
    works = Work.objects.all().order_by('-created')

    data = {
        'works': [work.json() for work in works],
    }

    return HttpResponse(json.dumps(data), content_type='application/json')

# 즐겨찾는 작품 목록
@require_http_methods(["POST"])
@csrf_exempt
def work_list_favorite(request):
    query_dict = request.POST
    print query_dict
    username = query_dict['username']
    user = User.objects.get(username=username)
    work_favorites = user.work_favorites

    data = {
        'works': [work_favorite.work.json() for work_favorite in work_favorites],
    }

    return HttpResponse(json.dumps(data), content_type='application/json')

# 댓글 목록
@require_http_methods(["POST"])
@csrf_exempt
def work_comment_list(request):
    query_dict = request.POST
    work_id = int(query_dict['work_id'])

    comments = WorkComment.objects.filter(work__id=work_id)

    data = {
        'comments': [comment.json() for comment in comments],
    }

    return HttpResponse(json.dumps(data), content_type='application/json')

# 댓글 추가
@require_http_methods(["POST"])
@csrf_exempt
def work_comment_add(request):
    query_dict = request.POST
    session_key = query_dict['session_key']
    username = query_dict['username']
    work_id = int(query_dict['work_id'])
    content = query_dict['content']

    s = SessionStore(session_key=session_key)

    # 유저가 세션값의 유저와 같으면 글 등록
    if username == s['username']:
        user = User.objects.get(username=s['username'])
        work = Work.objects.get(id=work_id)

        comment_instance = WorkComment(work=work, author=user, content=content)
        comment_instance.save()
        return return_success_json()
    else:
        return return_failed_json('Not Matching User')

# 댓글 삭제
@require_http_methods(["POST"])
@csrf_exempt
def work_comment_del(request):
    query_dict = request.POST
    session_key = query_dict['session_key']
    username = query_dict['username']
    work_id = int(query_dict['work_id'])
    comment_id = int(query_dict['comment_id'])

    s = SessionStore(session_key=session_key)

    if username == s['username']:
        user = User.objects.get(username=s['username'])
        work = Work.objects.get(id=work_id)
        comment = WorkComment.objects.get(id=comment_id)

        # 댓글 작성자와 사용자가 같을 경우 댓글 삭제
        if comment.author == user:
            comment.delete()
            return return_success_json()
        else:
            return return_failed_json('request user is not comment\'s author')
    else:
        return return_failed_json('Not Matching User')

@require_http_methods(["POST"])
@csrf_exempt
def work_rating(request):
    query_dict = request.POST
    work_id = int(query_dict['work_id'])

    try:
        work = Work.objects.get(id=work_id)
    except ObjectDoesNotExist:
        return return_failed_json('Not Existing Work')
    dict = {}

    # 평점 분석
    ratings = ChapterRating.objects.filter(chapter__work=work)
    avg_rating = ratings.aggregate(Avg('score'))['score__avg']
    if avg_rating:
        dict['rating'] = avg_rating
        dict['rating_number'] = ratings.count()
    else:
        dict['rating'] = 0.0
        dict['rating_number'] = 0

    return HttpResponse(json.dumps(dict), content_type='application/json')

'''
Chapter
    chapter_list : Chapter 목록
    chapter_view : 해당 chapter의 webview화면
    chapter_comment_list : 댓글 목록
    chapter_commnet_add : 댓글 추가
    chapter_comment_del : 댓글 삭제
    chapter_rating : 평점
    chapter_rating_add : 평점 추가
'''

@require_http_methods(["POST"])
@csrf_exempt
def chapter_list(request):
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

@require_http_methods(["POST"])
@csrf_exempt
def chapter_view(request):
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

# 댓글 목록
@require_http_methods(["POST"])
@csrf_exempt
def chapter_comment_list(request):
    query_dict = request.POST
    work_id = int(query_dict['work_id'])
    chapter_id = int(query_dict['chapter_id'])

    comments = ChapterComment.objects.filter(chapter__id=chapter_id) \
        .filter(chapter__work__id=work_id)
    chapter = Chapter.objects.get(id=chapter_id)

    data = {
        'rating': chapter.avg_rating,
        'comments': [comment.json() for comment in comments],
    }

    return HttpResponse(json.dumps(data), content_type='application/json')

# 댓글 추가
@require_http_methods(["POST"])
@csrf_exempt
def chapter_comment_add(request):
    query_dict = request.POST
    print query_dict
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

        comment_instance = ChapterComment(
            chapter=chapter, author=user, content=content)
        comment_instance.save()
        
        # 성공적으로 댓글 등록 후 해당 Chapter의 댓글 목록 리턴
        comments = ChapterComment.objects.filter(chapter__id=chapter_id) \
            .filter(chapter__work__id=work_id).order_by('-created')
        data = {
            'return_status': 'success',
            'comments': [comment.json() for comment in comments],
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return return_failed_json('Not Matching User')

# 댓글 삭제
@require_http_methods(["POST"])
@csrf_exempt
def chapter_comment_del(request):
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

@require_http_methods(["POST"])
@csrf_exempt
def chapter_rating(request):
    query_dict = request.POST
    username = query_dict['username']
    work_id = int(query_dict['work_id'])
    chapter_id = int(query_dict['chapter_id'])

    chapter = Chapter.objects.get(id=chapter_id)
    dict = {}

    # 평점 분석
    ratings = ChapterRating.objects.filter(chapter=chapter)
    avg_rating = ratings.aggregate(Avg('score'))['score__avg']
    if avg_rating:
        dict['avg_rating'] = avg_rating
        dict['rating_count'] = ratings.count()
    else:
        dict['avg_rating'] = 0.0
        dict['rating_count'] = 0

    # 해당 유저가 평가한 별점 있는지 확인, 있으면 True와 cur_user_rating추가해서 보냄 / 없으면 False만
    user = User.objects.get(username=username)
    if ChapterRating.objects.filter(chapter=chapter).filter(author=user).exists():
        dict['exist'] = True
        cur_user_rating = ChapterRating.objects.filter(chapter=chapter).get(author=user)
        dict['cur_user_rating'] = cur_user_rating.score
    else:
        dict['exist'] = False

    return HttpResponse(json.dumps(dict), content_type='application/json')

@require_http_methods(["POST"])
@csrf_exempt
def chapter_rating_add(request):
    query_dict = request.POST
    print query_dict
    session_key = query_dict['session_key']
    username = query_dict['username']
    work_id = int(query_dict['work_id'])
    chapter_id = int(query_dict['chapter_id'])
    rating = float(query_dict['rating'])

    s = SessionStore(session_key=session_key)

    if username == s['username']:
        user = User.objects.get(username=s['username'])
        work = Work.objects.get(id=work_id)
        chapter = Chapter.objects.get(work=work, id=chapter_id)

        if ChapterRating.objects.filter(chapter=chapter) \
                .filter(author=user).exists():
            rating_instance = ChapterRating.objects.get(
                chapter=chapter, author=user)
            rating_instance.score = rating
            rating_instance.save()
        else:
            rating_instance = ChapterRating.objects.create(
                chapter=chapter, author=user, score=rating)
            rating_instance.save()


        # 평점 분석
        ratings = ChapterRating.objects.filter(chapter=chapter)
        avg_rating = ratings.aggregate(Avg('score'))['score__avg']
        dict = {
            'return_status': 'success',
            'avg_rating': avg_rating,
            'rating': rating,
            'rating_count': ratings.count()
        }
        return HttpResponse(json.dumps(dict), content_type='application/json')
    else:
        return return_failed_json('Not Matching User')
