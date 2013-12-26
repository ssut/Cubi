#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from member.models import CubiUser

def create_member():
    print '\n== MentoringType모델 초기 데이터 설정 시작 ==\n'


    print '\n== MentoringType모델 초기 데이터 설정 완료 ==\n'

class Command(BaseCommand):
    args = ''
    help = 'MentoringType의 기본데이터 모델을 생성합니다'

    def handle(self, *args, **options):
        create_member()