#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

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

from cubi.functions import return_failed_json, return_success_json

import json

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

from .models import CubiUser
import django.core.exceptions

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        email = request.POST.get("email",None)
        password = request.POST.get("password",None)
        nickname = request.POST.get("nickname","큐비독자")
        # check absense of password, email
        if None in [ email, password]:
            raise exceptions.FieldError

        new_user = CubiUser.objects.create_user("1",email,"","",email,'M','','',nickname, password)
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
        return HttpResponse(json.dumps(
                    {"return_status":"failed",
                        "reason":"error in creating user"
                            }), content_type='application/json')




