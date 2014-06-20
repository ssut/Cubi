# -*- coding: utf-8 -*-
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import os

def version(request):
    filepath = os.path.join(os.path.dirname(__file__), 'version.txt')
    f = open(filepath)
    data = f.readlines()
    print data
    f.close()

    return HttpResponse(data)