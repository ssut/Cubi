#-*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# login
from django.contrib.auth import authenticate, login, logout

from work.models import Work
from .models import CubiUser
from member.forms import CubiUserSignupForm, CubiUserSigninForm, CubiUserConvertToAuthorForm, CubiUserEditForm, CubiUserPasswordChangeForm

import json

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
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_msg = u'로그인에 실패하였습니다. 이메일과 비밀번호를 확인해주세요'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/signin_failed.html', d, RequestContext(request))
        else:
            error_msg = u'로그인 양식의 내용이 올바르지 않습니다'
            return render_to_response('member/signin_failed.html', d, RequestContext(request))
    else:
        form = CubiUserSigninForm()
        d = {
            'form': form,
        }
        return render_to_response('member/signin.html', d, RequestContext(request))

def signout(request):
    logout(request)
    return render_to_response('member/signout.html')

def convert_to_author(request):
    user = request.user
    # user.type == '3' (작가전환대기)일 경우, 대기 페이지 표출
    # 그 외의 경우 Form 보여줌
    if request.method == 'POST':
        pass
    else:
        form = CubiUserConvertToAuthorForm()
        d = {
            'form': form,
        }
        return render_to_response('member/convert_to_author.html', d, RequestContext(request))

def member_info(request):
    user = request.user
    if request.method == 'POST':
        form = CubiUserEditForm(request.POST)
        if form.is_valid():
            # request한 user와 새로 들어온 form의 Password로 인증
            print user.email
            print form.cleaned_data['password']
            user = authenticate(username=user.email, password=form.cleaned_data['password'])
            if user is not None:
                email = form.cleaned_data['email']
                nickname = form.cleaned_data['nickname']
                password = form.cleaned_data['password']

                user.email = email
                user.username = email
                user.nickname = nickname
                user.set_password(password)
                user.save()

                d = {'return_status': 'success', 'user': user}

                return render_to_response('member/info_edit_success.html', d, RequestContext(request))
                
            else:
                # 이 부분은 message띄우면서 입력정보로 form다시 띄워주기
                error_msg = u'비밀번호를 확인해주세요'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/info_edit_failed.html', d, RequestContext(request))
        else:
            error_msg = u'회원정보 수정 양식의 내용이 올바르지 않습니다'
            return render_to_response('member/info_edit_failed.html', d, RequestContext(request))
    else:
        # print user.email
        # print user.nickname
        # print user.password
        form = CubiUserEditForm(initial={'email': user.email, 'nickname': user.nickname})
        d = {
            'form': form,
        }
        return render_to_response('member/info.html', d, RequestContext(request))

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = CubiUserPasswordChangeForm(request.POST)
        if form.is_valid():
            # request한 user와 새로 들어온 form의 Password로 인증
            print user.email
            print form.cleaned_data['original_password']
            user = authenticate(username=user.email, password=form.cleaned_data['original_password'])
            if user is not None:
                new_password = form.cleaned_data['new_password']
                new_password_confirm = form.cleaned_data['new_password_confirm']
                if new_password == new_password_confirm:
                    user.set_password(new_password)
                    user.save()
                    d = {'return_status': 'success', 'user': user}
                    return render_to_response('member/passwordchange_success.html', d, RequestContext(request))
                else:
                    error_msg = u'새 비밀번호와 비밀번호 확인이 일치하지 않습니다'
                    d = {'return_status': 'failed', 'reason': error_msg}
                    return render_to_response('member/passwordchange_failed.html', d, RequestContext(request))    
            else:
                # 이 부분은 message띄우면서 입력정보로 form다시 띄워주기
                error_msg = u'기존 비밀번호를 확인해주세요'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/passwordchange_failed.html', d, RequestContext(request))
        else:
            error_msg = u'비밀번호 변경 양식의 내용이 올바르지 않습니다'
            return render_to_response('member/passwordchange_failed.html', d, RequestContext(request))
    else:
        form = CubiUserPasswordChangeForm()
        d = {
            'form': form,
        }
        return render_to_response('member/passwordchange.html', d, RequestContext(request))

@csrf_exempt
def add_to_favorites(request):
    user = request.user
    _type = request.POST.get('type', None)
    _id = request.POST.get('id', None)
    if user is None or \
        _id is None or \
        _type is None or not request.is_ajax():
        return HttpResponse('{}', content_type="application/json")

    d = {
        'success': False,
        'message': '',
    }

    if _type == 'work':
        work = Work.objects.filter(id=_id)
        if not work.exists():
            d['message'] = '존재하지 않는 작품입니다.'
        elif user.check_favorites_exist(work[0]):
            d['message'] = '이미 즐겨찾기에 등록된 작품입니다.'
        else:
            user.add_favorites(work[0])
            d['success'] = True
    elif _type == 'author':
        author = CubiUser.objects.filter(id=_id)
        if not author.exists():
            d['message'] = '존재하지 않는 사용자입니다.'
        elif user.check_favorites_exist(author[0]):
            d['message'] = '이미 즐겨찾기에 등록된 작가입니다.'
        else:
            user.add_favorites(author[0])
            d['succes'] = True

    return HttpResponse(json.dumps(d), content_type="application/json")


def get_favorites(request):
    pass

