#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template import RequestContext

def index(request):
    return render_to_response('index.html')

def about(request):
    return render_to_response('about.html')


def reg_author(request):
    return render_to_response('reg_author.html')

def reg_work(request):
    return render_to_response('reg_work.html')