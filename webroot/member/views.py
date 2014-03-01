#-*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# login
from django.contrib.auth import authenticate, login, logout


from .models import CubiUser
from member.forms import CubiUserSignupForm, CubiUserSigninForm

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

def signin(request):
    if request.method == 'POST':
        form = CubiUserSigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_msg = u'로그인에 실패하였습니다. 이메일과 비밀번호를 확인해주세요'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/signin_failed.html')
        else:
            error_msg = u'로그인 양식의 내용이 올바르지 않습니다'
            return render_to_response('member/signin_failed.html')
    else:
        form = CubiUserSigninForm()
        d = {
            'form': form,
        }

        return render_to_response('member/signin.html', d, RequestContext(request))

def signout(request):
    logout(request)
    return render_to_response('member/signout.html')