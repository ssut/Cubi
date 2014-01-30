#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template import RequestContext

# Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from flynsarmy_paginator.paginator import FlynsarmyPaginator as Paginator

from board.models import Notice

def noticelist(request):
    page = request.GET.get('page')
    notice_list = Notice.objects.all()
    paginator = Paginator(notice_list, 2, adjacent_pages=3)

    try:
        notices = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        notices = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        notices = paginator.page(page)

    d = {
        'notices': notices,
    }

    return render_to_response('board/noticelist.html', d)