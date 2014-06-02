#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.db.models import Avg

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods