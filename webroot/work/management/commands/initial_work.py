# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from work.models import *

def create_work_category():
    work_category_list = [u'웹툰', u'만화', u'일러스트', u'소설']
    print '\n== WorkCategory모델 초기 데이터 설정 시작 ==\n'
    for work_category in work_category_list:
        work_category_instance, created = WorkCategory.objects.get_or_create(
            title=work_category)
        if created:
            work_category_instance.save()
            print u'\tWorkCategory [%s]\t\t생성' % (
                work_category_instance.title)
        else:
            print u'\tWorkCategory [%s]\t\t이미있음' % (
                work_category_instance.title)

    print '\n== WorkCategory모델 초기 데이터 설정 완료 ==\n'

def create_work():
    work_list = [
        {
            'category': WorkCategory.objects.get(title=u'웹툰'),
            'author': User.objects.get(id=1),
            'title': 'Test',
            'description': 'Test Description',
        }
    ]
    print '\n== Work모델 초기 데이터 설정 시작 ==\n'
    for work_dict in work_list:
        work_instance, created = Work.objects.get_or_create(
            work_num=0, category=work_dict['category'],
            author=work_dict['author'], title=work_dict['title'],
            description=work_dict['description'])
        if created:
            work_instance.save()
            print u'\tWork [%s]\t\t생성' % (work_instance.title)
        else:
            print u'\tWork [%s]\t\t이미있음' % (work_instance.title)

    print '\n== Work모델 초기 데이터 설정 완료 ==\n'

class Command(BaseCommand):
    args = ''

    def handle(self, *args, **options):
        create_work_category()
        create_work()
