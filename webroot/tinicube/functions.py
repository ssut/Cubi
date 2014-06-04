#-*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
# SITE_URL = settings.SITE_URL
#Custom User model
# try:
#     from django.contrib.auth import get_user_model
#     User = get_user_model()
# except ImportError:
#     from django.contrib.auth.models import User

# datetime
from datetime import datetime, time, date
import json


default_image = '/static/img/default_title.png'


### datetime -> String 변환 함수 ###
def day_to_string(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    else:
        return u'None'

def minute_to_string(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M')
    else:
        return u'None'

def time_to_string(value):
    if isinstance(value, datetime):
        return value.strftime('%H:%M')
    else:
        return u'None'


# 이미지 정보
def imageinfo(instance):
    return {
        'has_image': True if instance else False,
        'width': instance.width if instance else '',
        'height': instance.height if instance else '',
        'url': instance.url if instance else '',
    }

def imageinfo2(instance):
    return {
        'has_image': True if instance else False,
        'width': instance.width if instance else '',
        'height': instance.height if instance else '',
        'url': instance.url if instance else default_image,
    }

# json리턴
def return_failed_json(reason=''):
    dict = {'return_status': 'failed'}
    if reason != '' and reason != u'':
        dict['reason'] = reason
    return HttpResponse(json.dumps(dict), content_type='application/json')


def return_success_json(reason=''):
    dict = {'return_status': 'success'}
    if reason != '' and reason != u'':
        dict['reason'] = reason
    return HttpResponse(json.dumps(dict), content_type='application/json')
