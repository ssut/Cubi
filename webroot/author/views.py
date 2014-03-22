#-*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from author.forms import AddworkForm

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
    user = request.user
    if user.type != '2':
        return redirect('author:introduce')
    else:
        return render_to_response('author/index.html', RequestContext(request))

'''
작품 업로드
    1. 타입 선택
    2. 정보 입력
'''
def addwork(request):
    if request.method == 'POST':
        form = AddworkForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            print form.cleaned_data
            type = form.cleaned_data['type']
            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']
            introduce = form.cleaned_data['introduce']
            work_num = form.cleaned_data['work_num']
            image_cover = form.cleaned_data['image_cover']
            image_thumbnail = form.cleaned_data['image_thumbnail']
            image_loading = form.cleaned_data['image_loading']
            image_largeicon = form.cleaned_data['image_largeicon']
            image_smallicon = form.cleaned_data['image_smallicon']
            return HttpResponse('OK')

        else:
            error_msg = u'업로드 데이터가 잘못되었습니다'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('author/addwork_failed.html', d, RequestContext(request))
    else:
        form = AddworkForm()
        d = {'form': form}
        return render_to_response('author/addwork.html', d, RequestContext(request))

# 작품 업로드 1 - 타입 선택 (웹툰, 만화, 소설 등)
def addwork_select_type(request):
    if request.method == 'POST':
        query_dict = request.POST
        print query_dict
        type_value = query_dict.get('type', '')
        if type_value == 'webtoon_naver':
            return redirect('author:addwork_info')
        elif type_value == 'webtoon_daum':
            return redirect('author:addwork_info')
        else:
            error_msg = u'타입을 선택해주세요'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('author/addwork_select_type_failed.html', d, RequestContext(request))
    else:
        return render_to_response('author/addwork_select_type.html', RequestContext(request))

# 작품 업로드 2 - 해당 정보 입력
def addwork_info(request):
    if request.method == 'POST':
        form = AddworkInfoForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            print form.cleaned_data
            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']
            introduce = form.cleaned_data['introduce']
            work_num = form.cleaned_data['work_num']
            image_cover = form.cleaned_data['image_cover']
            image_thumbnail = form.cleaned_data['image_thumbnail']
            image_loading = form.cleaned_data['image_loading']
            image_largeicon = form.cleaned_data['image_largeicon']
            image_smallicon = form.cleaned_data['image_smallicon']

            


        else:
            error_msg = u'업로드 데이터가 잘못되었습니다'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('author/addwork_info_failed.html', d, RequestContext(request))
    else:
        form = AddworkInfoForm()
        d = {'form': form}
        return render_to_response('author/addwork_info.html', d, RequestContext(request))


