# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template import RequestContext

# Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from tinicube.paginator import FlynsarmyPaginator as Paginator

from .models import Notice

def notice_list(request):
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

    return render_to_response('board/notice_list_full.html', d,
                              RequestContext(request))

def notice_view(request, notice_id):
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

    notice = Notice.objects.get(id=notice_id)

    d = {
        'notices': notices,
        'notice': notice,
    }

    return render_to_response('board/notice_view.html', d,
                              RequestContext(request))
