from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# decorator
from django.views.decorators.csrf import csrf_exempt

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
