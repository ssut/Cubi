#-*- coding: utf-8 -*-
from django.conf import settings
from crawler.daum_webtoon import list as daum_list
from crawler.daum_leaguetoon import list as daum_league_list

# 통신 및 정규식, 파서
import urllib, urllib2
from bs4 import BeautifulSoup
import re

# 이미지처리
import Image
from cStringIO import StringIO
import os


media_path = settings.MEDIA_ROOT

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from work.models import *


thumbnail_path = 'image/thumbnail/'
cover_path = 'image/cover/'


def crawl_daumleague(comic_number, user):
    league_info = daum_league_list(comic_number)
    comic_title = league_info['comic_title']
    comic_author_name = league_info['comic_author_name']
    comic_genre = league_info['comic_genre']
    comic_url_img_title = league_info['comic_url_img_title']
    chapter_list = league_info['chapter_list']
    
    work_category, work_category_created = WorkCategory.objects.get_or_create(title=u'웹툰')
    work, work_created = Work.objects.get_or_create(category=work_category, title=comic_title, author=user)

    # 디렉토리 생성
    # image/cover/ 디렉토리 생성
    if not os.path.isdir(media_path + '/' + cover_path):
        os.mkdir(media_path + '/' + cover_path)

    # image/thumbnail/ 디렉토리 생성
    if not os.path.isdir(media_path + '/' + thumbnail_path):
        os.mkdir(media_path + '/' + thumbnail_path)

    # folder_name(image/thumbnail/(work.id)/ 디렉토리 생성
    thumbnail_folder_name = str(work.id)
    thumbnail_save_path = thumbnail_path + thumbnail_folder_name
    if not os.path.isdir(media_path + '/' + thumbnail_save_path):
        os.mkdir(media_path + '/' + thumbnail_save_path)

    for chapter in reversed(chapter_list):
        chapter_number = chapter['detail_num']
        chapter_title = chapter['title']
        chapter_url_thumbnail = chapter['url_thumbnail']
        chapter_date = chapter['date']

        if Chapter.objects.filter(reg_no=chapter_number).exists():
            print 'Chapter (reg_no:%s) is Exist!' % (chapter_number)
        else:
            print 'Chapter (reg_no:%s) start create' % (chapter_number)
            # 썸네일 저장
            url = chapter_url_thumbnail
            ext = '.jpg'
            save_ext = '.JPG'
            filename = media_path + '/' + thumbnail_path + str(work.id) + '/' + chapter_number + ext
            # urllib로 지정한 이름으로 이미지 다운로드 및 저장
            urllib.urlretrieve(url, filename)

            # imagefield에 들어갈 썸네일 주소
            filepath = thumbnail_path + str(work.id) + '/' + chapter_number + ext

            chapter_instance = Chapter.objects.create(reg_no=chapter_number, work=work, title=chapter_title, created=chapter_date, thumbnail=filepath)
            chapter_instance.save()
            print 'Chapter (reg_no:%s) end create' % (chapter_number)


# dogandrabbit
def crawl_daum(comic_title, user):
    list_info = daum_list(comic_title)
    title = list_info['comic_title']
    author_name = list_info['author_name']
    comic_description = list_info['comic_description']
    comic_grade = list_info['comic_grade']
    comic_genre = list_info['comic_genre']
    chapter_list = list_info['chapter_list']

    work_category, work_category_created = WorkCategory.objects.get_or_create(title=u'웹툰')
    work, work_created = Work.objects.get_or_create(category=work_category, title=title, author=user)

    # 디렉토리 생성
    # image/thumbnail/ 디렉토리 생성
    if not os.path.isdir(media_path + '/' + thumbnail_path):
        os.mkdir(media_path + '/' + thumbnail_path)

    # folder_name(image/thumbnail/(work.id)/ 디렉토리 생성
    thumbnail_folder_name = str(work.id)
    thumbnail_save_path = thumbnail_path + thumbnail_folder_name
    if not os.path.isdir(media_path + '/' + thumbnail_save_path):
        os.mkdir(media_path + '/' + thumbnail_save_path)


    for chapter in reversed(chapter_list):
        chapter_number = chapter['chapter_number']
        chapter_title = chapter['title']
        chatper_strdate = chapter['strdate']
        chapter_short_title = chapter['short_title']
        chapter_date = chapter['date']
        chapter_url_thumbnail = chapter['url_thumbnail']
        chapter_url = chapter['chapter_url']

        if Chapter.objects.filter(reg_no=chapter_number).exists():
            print 'Chapter (reg_no:%s) is Exist!' % (chapter_number)
        else:
            print 'Chapter (reg_no:%s) start create'
            url = chapter_url_thumbnail

            ext = '.jpg'
            save_ext = '.JPG'

            filename = media_path + '/' + str(work.id) + '/' + chapter_number + ext
            # urllib로 지정한 이름으로 이미지 다운로드 및 저장
            urllib.urlretrieve(url, filename)


            chapter_instance = Chapter.objects.create(reg_no=chapter_number, work=work, title=chapter_title, created=chapter_date)
            chapter_instance.save()
            print 'Chapter (reg_no:%s) end create'