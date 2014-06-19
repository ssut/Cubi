# -*- coding: utf-8 -*-
import json

import django.core.exceptions

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Custom User model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Authenticate
from django.contrib.auth import authenticate, login

from tinicube.functions import return_failed_json, return_success_json

from author.models import AuthorInfo
from work.models import Work

'''
author_info
    작가정보
login
    로그인
signup
    회원가입
all_author_list
    모든 작가 리스트
'''
@csrf_exempt
@require_http_methods(["POST"])
def author_info(request):
    query_dict = request.POST
    user_id = query_dict['user_id']

    user = User.objects.get(id=user_id)
    author_info = AuthorInfo.objects.get(user=user)

    works = Work.objects.filter(author=user)

    dict = {
        'author_info': author_info.json(),
        'works': [work.json() for work in works],
    }
    return HttpResponse(json.dumps(dict), content_type='application/json')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        query_dict = request.POST
        print query_dict
        username = query_dict['username']
        password = query_dict['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            cur_user = user
        else:
            return return_failed_json('Login Failed')

        user_data = cur_user.json()
        data = {
            'user_data': user_data,
        }

        s = SessionStore()
        s['username'] = username
        s.save()
        session_key = s.session_key

        data['session_key'] = session_key

        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        nickname = request.POST.get("nickname", "큐비독자")
        # check absense of password, email
        if None in [email, password]:
            raise exceptions.FieldError

        args = ["1", email, "", "", email, 'M', '', '', nickname, password]
        new_user = TinicubeUser.objects.create_user(*args)
        data = {
            'user_data': new_user.json()
        }
        s = SessionStore()
        s['username'] = email
        s.save()
        session_key = s.session_key
        data['session_key'] = session_key
        return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        result = {
            "return_status": "failed",
            "reason": "error in creating user"
        }
        return HttpResponse(json.dumps(result),
                            content_type='application/json')

@csrf_exempt
@require_http_methods(["POST"])
def all_author_list(request):
    query_dict = request.POST
    authors = User.objects.filter(type='2').filter(is_superuser=False).order_by('-date_joined')

    data = {
        'authors': [author.json() for author in authors],
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST"])
def favorite_author_list(request):
    query_dict = request.POST
    username = query_dict['username']
    cur_user = User.objects.get(username=username)
    cur_user_favorites = cur_user.author_favorites

    data = {
        'authors': [favorite.author.json() for favorite in cur_user_favorites],
    }
    return HttpResponse(json.dumps(data), content_type='application/json')