# -*- coding: utf-8 -*-
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime, timedelta

from work import crawl as crawler

from .models import *

# 매 분마다 실행되는 작업
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def crawl_webtoon():
    item = ChapterQueue.filter(is_checked=False).order_by('created_at')[0]
    result = crawler.crawl(
        type=item.target, comic_number=item.comic_number,
        chapter_number=item.chapter_number, user=item.user)
    item.is_checked = True
    item.checked_at = datetime.now()
    item.is_succeeded = result
    item.save()

# 1시간마다 실행되는 작업 (연속적으로 크롤링해야 할 때)
@periodic_task(run_every=crontab(hour="*", minute="0", day_of_week="*"))
def crawl_periodic():
    date = datetime.now()
    date.replace(minute=0, second=0, microsecond=0)
    list = ChapterPeriodicQueue.filter(last_run_at__lte=date, enabled=True)
    for item in list:
        result = crawler.crawl(
            type=item.target, comic_number=item.comic_number, user=item.user)
        item.last_run_at = datetime.now()
        item.last_run_result = result
        item.save()
