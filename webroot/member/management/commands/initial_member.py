#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from member.models import CubiUser

user_list = [
    {
        'type': '1',
        'username': 'darjeeling',
        'nickname': 'darjeeling',
        'first_name': u'권한',
        'last_name': u'배',
        'email': 'baekwonhan@cubi.in',
        'gender': 'M',
        'tel': '000',
        'access_token': '000',
    },
    {
        'type': '1',
        'username': 'arcanelux',
        'nickname': 'Arcanelux',
        'first_name': u'한영',
        'last_name': u'이',
        'email': 'leehanyeong@cubi.in',
        'gender': 'M',
        'tel': '000',
        'access_token': '000',
    },
    {
        'type': '1',
        'username': 'baejujin',
        'nickname': 'baejujin',
        'first_name': u'주진',
        'last_name': u'배',
        'email': 'baejujin@cubi.in',
        'gender': 'M',
        'tel': '000',
        'access_token': '000',
    },
    {
        'type': '1',
        'username': 'ssut',
        'nickname': 'ssut',
        'first_name': u'수훈',
        'last_name': u'한',
        'email': 'hansuhun@cubi.in',
        'gender': 'M',
        'tel': '000',
        'access_token': '000',
    },
]
def create_member():
    print '\n== Member모델 초기 데이터 설정 시작 ==\n'
    for user_dict in user_list:
        user_instance, created = CubiUser.objects.get_or_create(type=user_dict['type'], username=user_dict['username'], nickname=user_dict['nickname'], gender=user_dict['gender'], tel=user_dict['tel'], access_token=user_dict['access_token'], last_name=user_dict['last_name'], first_name=user_dict['first_name'])
        if created:
            user_instance.save()
            print u'\tUser [%s%s]\t\t생성' % (user_instance.last_name, user_instance.first_name)
        else:
            print u'\tUser [%s%s]\t\t이미있음' % (user_instance.last_name, user_instance.first_name)



    print '\n== Member모델 초기 데이터 설정 완료 ==\n'

class Command(BaseCommand):
    args = ''

    def handle(self, *args, **options):
        create_member()