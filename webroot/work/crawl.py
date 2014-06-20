# -*- coding: utf-8 -*-
import grp
import logging
import os
import pwd
import re
import urllib
import urllib2

from django.conf import settings
from django.utils.timezone import now

from crawler import daum_leaguetoon as DaumLeaguetoon
from crawler.naver_webtoon import NaverWebtoon

# 통신 및 정규식, 파서
from bs4 import BeautifulSoup


from cStringIO import StringIO
from datetime import datetime
from logging import handlers

from PIL import Image as PIL_Image

# Log
cur_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(cur_path)

# 서비스용, 로컬 분리
# if settings.DEBUG is False:
#     log_file_path = '/srv/www/tinicube_logger.txt'
# else:
#     log_file_path = os.path.join(base_path, 'logger.txt')
log_file_path = '/tmp/tinicube_logger.txt'


log = logging.getLogger('MyLogger')
log.setLevel(logging.DEBUG)
# 콘솔 출력과 파일 출력을 같이 사용
conh = logging.StreamHandler()
conh.setLevel(logging.DEBUG)
fileh = handlers.RotatingFileHandler(
    log_file_path, maxBytes=1024, backupCount=0)  # 로그 로테이션을 사용
log.addHandler(conh)
log.addHandler(fileh)

REAL_PATH = ''
FIELD_PATH = ''
MEDIA_PATH = settings.MEDIA_ROOT

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from .models import *
from member.models import *
'''
폴더구조
    날짜기준으로 생성
    기본 : yyyymmdd/
    Work - Webtoon : 기본/work/webtoon/
        썸네일 : (work.id)_(chapter_number)_thumbnail.jpg

'''
# 디렉토리 생성
def make_directory():
    global REAL_PATH, FIELD_PATH
    today = now().today()
    today_str = today.strftime('%Y%m%d')
    REAL_PATH = os.path.join(MEDIA_PATH, today_str, 'work', 'webtoon')
    FIELD_PATH = os.path.join(today_str, 'work', 'webtoon')

    if not os.path.exists(REAL_PATH):
        os.makedirs(REAL_PATH)
        if not DEBUG:
            try:
                uid = pwd.getpwnam('www-data').pw_uid
                gid = grp.getgrnam('www-data').gr_gid
                os.chown(REAL_PATH, uid, gid)
            except:
                pass

# make_directory에서 지정된 전역변수 path를 이용, MEDIA_PATH를 포함한 저장할 파일명의 path를 반환
def get_save_path(filename):
    global REAL_PATH
    return os.path.join(REAL_PATH, filename)

# ImageField, FileField에 저장할 path반환
def get_field_path(filename):
    global FIELD_PATH
    return os.path.join(FIELD_PATH, filename)

# 웹툰 Work 생성 또는 리턴
def get_work(comic_number, user, type):
    if type == ChapterQueue.NAVER:
        comic_info = NaverWebtoon().info(comic_number)
    elif type == ChapterQueue.DAUM:
        comic_info = DaumLeaguetoon.info(comic_number)

    comic_title = comic_info['title']
    comic_title_image = comic_info['title_image']
    comic_author_name = comic_info['author']
    comic_description = comic_info['description']
    comic_genre = comic_info['genre']

    work_category, work_category_created = WorkCategory.objects.get_or_create(
        title=u'웹툰')
    work, work_created = Work.objects.get_or_create(
        work_num=comic_number,
        work_target=type,
        category=work_category,
        title=comic_title,
        description_full=comic_description,
        author=user)

    work.description_full = comic_description
    work.save()

    return work

# Chapter List의 구성요소인 chapter_dict의 정보로 Chapter인스턴스 생성 후 저장, 리턴
def make_chapter(chapter_dict, work, type):
    chapter_number = chapter_dict['no']
    chapter_title = chapter_dict['title']
    chapter_thumbnail = chapter_dict['thumbnail']
    chapter_date = chapter_dict['date']

    chapter_instance, chapter_created = Chapter.objects.get_or_create(
        reg_no=chapter_number, work=work)
    if not chapter_created:
        pass
    else:
        # ImageField에 저장될 thumbnail이름
        filename = u'%s_%s_thumbnail.jpg' % (work.id, chapter_number)
        fieldpath = get_field_path(filename)
        # 다운로드 받을 전체 경로(MEDIA_PATH포함)
        filepath = get_save_path(filename)
        with open(filepath, 'wb') as stream:
            stream.write(chapter_thumbnail.read())
        chapter_thumbnail.close()

        setattr(chapter_instance, 'reg_no', chapter_number)
        setattr(chapter_instance, 'work', work)
        setattr(chapter_instance, 'title', chapter_title)
        setattr(chapter_instance, 'created', chapter_date)
        setattr(chapter_instance, 'thumbnail', fieldpath)
        chapter_instance.save()

    return chapter_instance, chapter_created

def save_chapter_contents(chapter_instance, work, images, type):
    log.debug("- Save Chapter Contents"
              " (Work:%s, ChapterNum:%s, ImagesNum:%s, Type:%s) -" %
              (work, str(chapter_instance.reg_no), len(images), type))
    chapter_number = chapter_instance.reg_no
    crop_list = get_croplist(images)

    # 크롭된 이미지 저장 후 Content instance 생성
    for i, image in enumerate(crop_list):
        log.debug(' Crop List[%s] Process')

        ext = "jpg"
        # 파일명 지정 (GIF, 그외)
        if image.format == 'GIF':
            ext = "gif"
        filename = u'%s_%s_%02d_%02d.%s' % (
            work.id, chapter_number, 0, i + 1, ext)

        log.debug('  Current Image(FileName:%s) Instance create' % (filename))
        fieldpath = get_field_path(filename)
        filepath = get_save_path(filename)

        # 이미지 저장 (GIF, 그외)
        if image.format == 'GIF':
            image.save(filepath, 'GIF')
        else:
            image.save(filepath, 'JPEG', quality=90)

        image_instance = Image(chapter=chapter_instance,
                               sequence=i, image=fieldpath)
        image_instance.save()
        log.debug('  Current Image(FileName:%s) Instance saved' % (filename))

def get_croplist(images):
    log.debug('  - Get Croplist (ImagesNum:%s) -' % (len(images)))
    combined_image = None
    image_list, crop_list = [], []
    image_width, image_height = 0, []
    # StringIO 에 담겨져있는 이미지를 PIL 이미지로 바꿔서 리스트에 저장
    for i, image in enumerate(images):
        log.debug('%06sCurrent Image[%s] Process start' % ('', i))
        try:
            img = PIL_Image.open(images[i])
            log.debug('%08sCurrent Image[%s] Open success' % ('', i))
        except Exception, e:
            log.debug('%08sCurrent Image[%s] Open failed' % ('', i))
            pass

        if img.format == 'GIF':
            log.debug('%08sCurrent Image[%s] format is %s' % (
                '', i, img.format))
            log.debug('%08sGIF File crop skip' % (''))
            crop_list.append(img)
        else:
            if img.mode != 'RGB':
                log.debug('%08sCurrent Image[%s] mode is %s' % (
                    '', i, img.mode))
                log.debug('%08sCurrent Image[%s] mode is not RGB' % (
                    '', i))
                log.debug('%08sCurrent Image[%s] mode convert to RGB' % (
                    '', i))

            log.debug('%10sCrop Image every 2000px start' % (''))
            while img.size[1] > 0:
                if img.size[1] > 2000:
                    log.debug('%12sRemain height > 2000' % (''))
                    crop_height = 2000
                else:
                    log.debug('%12sRemain height < 2000, value:%s' % (
                        '', img.size[1]))
                    crop_height = img.size[1]

                box1 = (0, 0, img.size[0], crop_height)
                crop_list.append(img.crop(box1))

                box2 = (0, crop_height, img.size[0], img.size[1])
                img = img.crop(box2)
                log.debug('%14sCrop Image, Remain height:%s' % (
                    '', img.size[1]))
            log.debug('%10sCrop Image every 2000px end' % (''))

    log.debug('      Current Image[%s] Process end\n' % (i))
    return crop_list

"""
웹툰 크롤링
TYPE: ChapterQueue.NAVER, ChapterQueue.DAUM
crawl(type=ChapterQueue.TYPE, comic_number=i32, user=User):
    크롤되지 않은 모든 웹툰을 크롤링함
crawl(type=ChapterQueue.TYPE, comic_number=i32, chapter_number=i32, user=User):
    한 화만 선택헤서 크롤링함
"""
def crawl(*args, **kargs):
    # 웹툰 Work 생성
    type = kargs['type']
    comic_number = kargs['comic_number']
    user = kargs['user']

    # Work instance 가져오기
    work = get_work(comic_number, user, type)

    # 디렉토리 생성
    make_directory()
    args_len = len(kargs)
    if args_len == 3:  # 크롤되지 않은 모든 웹툰 크롤링
        # Chapter List 가져오기
        if type == ChapterQueue.NAVER:
            chapter_list = NaverWebtoon().list(comic_number)
        elif type == ChapterQueue.DAUM:
            chapter_list = DaumLeaguetoon.list(comic_number)

        last_result = False
        for chapter in chapter_list:
            if not Chapter.objects.filter(
                    reg_no=chapter['no'], work=work).exists():
                try:
                    last_result = crawl(
                        type=type, comic_number=comic_number,
                        chapter_number=chapter['no'], user=user)
                except:
                    pass

        return last_result
    elif args_len == 4:  # 한 화만 선택해서 크롤링
        chapter_number = kargs['chapter_number']
        # Chapter Dictionary(detail) 가져오기
        if type == ChapterQueue.NAVER:
            chapter_dict = NaverWebtoon().detail(comic_number, chapter_number)
        elif type == ChapterQueue.DAUM:
            chapter_dict = DaumLeaguetoon.detail(chapter_number)

        # Chapter 생성
        cur_chapter, chapter_created = make_chapter(chapter_dict, work, type)
        if chapter_created:
            save_chapter_contents(cur_chapter, work, chapter_dict['images'],
                                  type)
            return True
        else:
            return False
