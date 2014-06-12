# -*- coding: utf-8 -*-
import json

from datetime import datetime, time, date

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404

# datetime -> String 변환 함수 ###
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


def imageinfo(instance, url=None):
    dict = {
        'has_image': True if instance else False,
        'width': instance.width if instance else '',
        'height': instance.height if instance else '',
        'url': instance.url if instance else url,
    }
    if not instance and url is None:
        dict['url'] = ''
    return dict

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
