# -*- encoding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseForbidden, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

# decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .backends import FacebookAuthBackend
from .models import TinicubeUser
from .forms import TinicubeUserSignupForm, TinicubeUserSigninForm, \
    TinicubeUserConvertToAuthorForm, TinicubeUserEditForm, \
    TinicubeUserPasswordChangeForm
from work.models import Work

from tinicube import settings

from rauth import OAuth2Service

facebook = OAuth2Service(
    client_id=settings.FACEBOOK_APP_ID,
    client_secret=settings.FACEBOOK_API_SECRET,
    name='tinicube',
    authorize_url='https://graph.facebook.com/oauth/authorize',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    base_url='https://graph.facebook.com/')


def signup(request):
    if request.method == 'POST':
        form = TinicubeUserSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']

            if TinicubeUser.objects.filter(email=email).exists():
                error_msg = u'이미 사용중인 이메일 입니다'
                d = {'form':
                     form, 'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/signup.html', d,
                                          RequestContext(request))
            elif TinicubeUser.objects.filter(nickname=nickname).exists():
                error_msg = u'이미 사용중인 닉네임 입니다'
                d = {'form':
                     form, 'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/signup.html', d,
                                          RequestContext(request))
            else:
                user = TinicubeUser.objects.create_user(
                    "1", email, "", "", email, 'M', '', '', nickname, password)
                d = {'user': user}
                return render_to_response('member/signup_complete.html', d,
                                          RequestContext(request))
        else:
            error_msg = u'가입양식의 내용이 올바르지 않습니다'
            d = {'return_status': 'failed', 'reason': error_msg}
            return render_to_response('member/signup.html', d,
                                      RequestContext(request))
    else:
        form = TinicubeUserSignupForm()
        d = {
            'form': form,
        }
        return render_to_response('member/signup.html', d,
                                  RequestContext(request))

def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = TinicubeUserSigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_msg = u'로그인에 실패하였습니다. 이메일과 비밀번호를 확인해주세요'
                d = {
                    'form': form,
                    'error': error_msg,
                }
                return render_to_response('member/signin.html', d,
                                          RequestContext(request))
        else:
            error_msg = u'로그인 양식의 내용이 올바르지 않습니다'
            d = {
                'form': form,
                'error': error_msg,
            }
            return render_to_response('member/signin.html', d,
                                      RequestContext(request))
    else:
        form = TinicubeUserSigninForm()
        d = {
            'form': form,
        }
        return render_to_response('member/signin.html', d,
                                  RequestContext(request))


def signin_with_facebook(request):
    redirect_uri = request.build_absolute_uri(
        reverse('member:signin_with_facebook_callback'))
    params = {
        'scope': 'read_stream',
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }

    url = facebook.get_authorize_url(**params)
    return redirect(url)


def signin_with_facebook_callback(request):
    redirect_uri = request.build_absolute_uri(
        reverse('member:signin_with_facebook_callback'))
    code = request.GET.get('code', '')

    try:
        session = facebook.get_auth_session(data={
            'code': code,
            'redirect_uri': redirect_uri
        })
    except Exception, e:
        resp = "<script> alert(\"페이스북 연결 실패\"); location.replace(\"" + \
               reverse('signin') + "\") </script>"
        return HttpResponse(resp)

    fbid = session.get('me').json()['id']
    user = TinicubeUser.objects.filter(access_token=fbid)
    if user.exists():
        user = authenticate(user_id=user[0].id)
        print user
        login(request, user)
        return redirect('index')
    else:
        resp = "<script> alert(\"일치하는 계정 없음\"); location.replace(\"" + \
               reverse('signin') + "\") </script>"
        return HttpResponse(resp)


@login_required
def signout(request):
    logout(request)
    return render_to_response('member/signout.html')


@login_required
def connect_facebook(request):
    redirect_uri = request.build_absolute_uri(
        reverse('member:connect_facebook_callback'))
    params = {
        'scope': 'read_stream',
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }

    url = facebook.get_authorize_url(**params)
    return redirect(url)

@login_required
def connect_facebook_callback(request):
    user = request.user
    redirect_uri = request.build_absolute_uri(
        reverse('member:connect_facebook_callback'))
    code = request.GET.get('code', '')

    try:
        session = facebook.get_auth_session(data={
            'code': code,
            'redirect_uri': redirect_uri
        })
    except Exception, e:
        resp = "<script> alert(\"페이스북 연결 실패\"); location.replace(\"" + \
               reverse('member_info') + "\") </script>"
        return HttpResponse(resp)

    fbid = session.get('me').json()['id']
    user.access_token = fbid
    user.save()
    resp = "<script> alert(\"페이스북 연결 완료\"); location.replace(\"" + \
           reverse('member_info') + "\") </script>"
    return HttpResponse(resp)

@login_required
def disconnect_facebook(request):
    user = request.user
    user.access_token = ''
    user.save()

    resp = "<script> alert(\"페이스북 연결 해제 완료\"); location.replace(\"" + \
           reverse('member_info') + "\") </script>"
    return HttpResponse(resp)

def convert_to_author(request):
    user = request.user
    # user.type == '3' (작가전환대기)일 경우, 대기 페이지 표출
    # 그 외의 경우 Form 보여줌
    if request.method == 'POST':
        pass
    else:
        form = TinicubeUserConvertToAuthorForm()
        d = {
            'form': form,
        }
        return render_to_response('member/convert_to_author.html', d,
                                  RequestContext(request))


@login_required
def member_info(request):
    user = request.user
    if request.method == 'POST':
        form = TinicubeUserEditForm(request.POST)
        if form.is_valid():
            # request한 user와 새로 들어온 form의 Password로 인증
            print user.email
            print form.cleaned_data['password']
            user = authenticate(username=user.email,
                                password=form.cleaned_data['password'])
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

                return render_to_response('member/info_edit_success.html', d,
                                          RequestContext(request))
            else:
                # 이 부분은 message띄우면서 입력정보로 form다시 띄워주기
                error_msg = u'비밀번호를 확인해주세요'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response('member/info_edit_failed.html', d,
                                          RequestContext(request))
        else:
            error_msg = u'회원정보 수정 양식의 내용이 올바르지 않습니다'
            return render_to_response('member/info_edit_failed.html', d,
                                      RequestContext(request))
    else:
        form = TinicubeUserEditForm(
            initial={'email': user.email, 'nickname': user.nickname})
        d = {
            'form': form,
        }
        return render_to_response('member/info.html', d,
                                  RequestContext(request))


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = TinicubeUserPasswordChangeForm(request.POST)
        if form.is_valid():
            # request한 user와 새로 들어온 form의 Password로 인증
            print user.email
            print form.cleaned_data['original_password']
            user = authenticate(
                username=user.email,
                password=form.cleaned_data['original_password'])
            if user is not None:
                new_password = form.cleaned_data['new_password']
                new_password_confirm = form.cleaned_data[
                    'new_password_confirm']
                if new_password == new_password_confirm:
                    user.set_password(new_password)
                    user.save()
                    d = {'return_status': 'success', 'user': user}
                    return render_to_response(
                        'member/passwordchange_success.html',
                        d, RequestContext(request))
                else:
                    error_msg = u'새 비밀번호와 비밀번호 확인이 일치하지 않습니다'
                    d = {'return_status': 'failed', 'reason': error_msg}
                    return render_to_response(
                        'member/passwordchange_failed.html',
                        d, RequestContext(request))
            else:
                # 이 부분은 message띄우면서 입력정보로 form다시 띄워주기
                error_msg = u'기존 비밀번호를 확인해주세요'
                d = {'return_status': 'failed', 'reason': error_msg}
                return render_to_response(
                    'member/passwordchange_failed.html',
                    d, RequestContext(request))
        else:
            error_msg = u'비밀번호 변경 양식의 내용이 올바르지 않습니다'
            return render_to_response(
                'member/passwordchange_failed.html',
                d, RequestContext(request))
    else:
        form = TinicubeUserPasswordChangeForm()
        d = {
            'form': form,
        }
        return render_to_response('member/passwordchange.html', d,
                                  RequestContext(request))

@csrf_exempt
@login_required
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
        author = TinicubeUser.objects.filter(id=_id)
        if not author.exists():
            d['message'] = '존재하지 않는 사용자입니다.'
        elif user.check_favorites_exist(author[0]):
            d['message'] = '이미 즐겨찾기에 등록된 작가입니다.'
        else:
            user.add_favorites(author[0])
            d['succes'] = True

    return HttpResponse(json.dumps(d), content_type="application/json")


@login_required
def get_favorites(request):
    user = request.user
    if user is None or not request.is_ajax():
        return HttpResponse('{ "success": false }',
                            content_type="application/json")

    d = {
        'success': False,
        'data': {
            'works': [],
            'authors': [],
        },
    }

    try:
        d['data']['works'] = [{
            'id': i.work.id,
            'title': i.work.title,
            'last_upload': i.work.last_upload.strftime('%Y-%m-%d'),
            'author': i.work.author.nickname
        } for i in user.work_favorites]
        d['data']['authors'] = [{
            'id': i.author.id,
            'name': i.author.nickname
        } for i in user.author_favorites]
        d['success'] = True
    except Exception, e:
        print e

    return HttpResponse(json.dumps(d), content_type="application/json")


@login_required
def delete_account(request):
    if request.method != 'POST' or not request.is_ajax():
        return
    referer = request.META.get('HTTP_REFERER')
    if not referer or referer.find('/member/info') == -1:
        return

    try:
        user = request.user
        logout(request)
        user.delete()
    except:
        d = {'success': False, 'message': '계정 삭제 도중 오류가 발생했습니다.'}
    else:
        d = {'success': True, 'message': '계정이 삭제되었습니다.'}
    return HttpResponse(json.dumps(d), content_type="application/json")
