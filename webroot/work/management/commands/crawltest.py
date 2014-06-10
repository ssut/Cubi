# from work.models import *

#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
class Command(BaseCommand):
    args = ''

    def handle(self, *args, **options):
        from work import crawl as crawler
        from work.models import ChapterQueue
        from member.models import TinicubeUser

        user = TinicubeUser.objects.get(id=1)
        if args[0] == 'naver' or args[0] == 'NAVER':
            type = ChapterQueue.NAVER
        elif args[0] == 'daum' or args[0] == 'DAUM':
            type = ChapterQueue.DAUM

        comic_number = str(args[1])
        print type
        print comic_number

        crawler.crawl(type=type, comic_number=comic_number, user=user)
