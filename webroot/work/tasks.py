#-*- coding: utf-8 -*-
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime, timedelta

from .models import *

# 매 분마다 실행되는 작업
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def crawl_webtoon():
    # 큐에서 처리할 작업을 하나 가져온다
    queue = ChapterQueue.filter(is_checked=False).order_by('created_at')[0]

    crawler = None
    if queue.target == u'네이버':
        return

    # TODO.
    # 크롤 함수 완성 후에 계속 개발 진행
    # 여러 인수를 받는 옵션이 필요함