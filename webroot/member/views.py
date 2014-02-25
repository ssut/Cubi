#-*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from .models import CubiUser
from member.forms import CubiUserSignupForm

def signup(request):
    if request.method == 'POST':
        form = CubiUserSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']

            if CubiUser.objects.filter(email=email).exists():
                error_msg = u'이미 사용중인 이메일 입니다'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/signup_failed.html', d, RequestContext(request))
            elif CubiUser.objects.filter(nickname=nickname).exists():
                error_msg = u'이미 사용중인 닉네임 입니다'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/signup_failed.html', d, RequestContext(request))
            else:
                user = CubiUser.objects.create_user("1",email,"","",email,'M','','',nickname, password)
                d = {'user': user}
                return render_to_response('member/signup_complete.html', d, RequestContext(request))
        else:
            error_msg = u'가입양식의 내용이 올바르지 않습니다'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('member/signup_failed.html', d, RequestContext(request))
    else:
        form = CubiUserSignupForm()

        d = {
            'form': form,
        }

        return render_to_response('member/signup.html', d, RequestContext(request))