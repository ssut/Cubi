from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from cubi.functions import day_to_string
from cubi.settings import MEDIA_URL

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from author.models import WaitConvert

def index(request):
    return render_to_response('adminstrator/index.html', RequestContext(request))

def wait_convert_list(request):
    waiting_list = WaitConvert.objects.all().order_by('-created')
    d = {
        'waiting_list': waiting_list,
    }

    return render_to_response('adminstrator/wait_convert_list.html', d, RequestContext(request))

def convert(request, user_id, boolean):
    user = User.objects.get(id=user_id)
    if WaitConvert.objects.filter(user=user).exists():
        waitconvert = WaitConvert.objects.get(user=user)
        try:
            if boolean == 'true':
                user.type = '2'
            elif boolean == 'false':
                user.type == '1'
            user.save()
            waitconvert.delete()
            return render_to_response('adminstrator/convert_success.html', d, RequestContext(request))
        except:
            return render_to_response('adminstrator/convert_failed.html', d, RequestContext(request))
    else:
        return render_to_response('adminstrator/convert_failed.html', d, RequestContext(request))

def convert_deny(request, user_id):
    user = User.objects.get(id=user_id)
    if WaitConvert.objects.filter(user=user).exists():
        waitconvert = WaitConvert.objects.filter(user=user)
        try:
            user.type = '1'
            user.save()
            waitconvert.delete()
            return render_to_response('adminstrator/convert_success.html', d, RequestContext(request))
        except:
            return render_to_response('adminstrator/convert_failed.html', d, RequestContext(request))
    else:
        return render_to_response('adminstrator/convert_failed.html', d, RequestContext(request))
