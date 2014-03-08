#-*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# 작품 업로드 소개
def introduce(request):
    return render_to_response('author/introduce.html', RequestContext(request))

# 작품 업로드 약관 동의
def agreement(request):
    if request.method == 'POST':
        query_dict = request.POST
        print query_dict
        agreement_value = query_dict.get('agreement', 'false')
        if agreement_value == 'true':
            user = request.user
            user.type = '2'
            user.save()
            return redirect('author:index')
        else:
            error_msg = u'약관에 동의하셔야 합니다'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('author/agreement_failed.html', d, RequestContext(request))
    else:
        return render_to_response('author/agreement.html', RequestContext(request))

# 작품 업로드 메인
def index(request):
    return render_to_response('author/index.html', RequestContext(request))
