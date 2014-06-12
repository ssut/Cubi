# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from board.models import *
modelname = u'Board'

def create_notice():
    dict_list = [
        {
            'title': u'공지사항1',
            'content': u'공지사항1 입니다',
        },
        {
            'title': u'공지사항2',
            'content': u'공지사항2 입니다',
        },
        {
            'title': u'공지사항3',
            'content': u'공지사항3 입니다',
        },
        {
            'title': u'공지사항4',
            'content': u'공지사항4 입니다',
        },
        {
            'title': u'공지사항5',
            'content': u'공지사항5 입니다',
        },
        {
            'title': u'공지사항6',
            'content': u'공지사항6 입니다',
        },
        {
            'title': u'공지사항7',
            'content': u'공지사항7 입니다',
        },
        {
            'title': u'공지사항8',
            'content': u'공지사항8 입니다',
        },
        {
            'title': u'공지사항9',
            'content': u'공지사항9 입니다',
        },
        {
            'title': u'공지사항10',
            'content': u'공지사항10 입니다',
        },
        {
            'title': u'공지사항11',
            'content': u'공지사항11 입니다',
        },
        {
            'title': u'공지사항12',
            'content': u'공지사항12 입니다',
        },
        {
            'title': u'공지사항13',
            'content': u'공지사항13 입니다',
        },
    ]
    create_model(u'Notice', Notice, dict_list)


def create_model(name, cur_model, dict_list):
    model_list = dict_list
    modelname = name
    model = cur_model

    print u'\n - %s 생성 시작 -' % (modelname)
    for model_dict in model_list:
        key, value = str(model_dict.keys()[0]), str(model_dict.values()[0])
        if model.objects.filter(**model_dict).exists():
            try:
                print u'   %s (%s:%s) 은(는) 이미 있습니다' % (model, key, value)
            except:
                print u'   %s 은(는) 이미 있습니다' % (model)
        else:
            new_instance = model(**model_dict)
            new_instance.save()
            try:
                print u'   %s (%s:%s) 생성되었습니다' % (model, key, value)
            except:
                print u'   %s 생성되었습니다' % (model)
    print u' - %s 생성 완료 -\n' % (modelname)


class Command(BaseCommand):
    args = ''

    def handle(self, *args, **options):
        print u'\n== %s 모델 초기 데이터 설정 시작 ==' % (modelname)
        create_notice()
        print u'== %s 모델 초기 데이터 설정 완료 ==\n' % (modelname)
