#-*- coding: utf-8 -*-
from django.conf import settings
from crawler import daum_leaguetoon as DaumLeaguetoon
from crawler.naver_webtoon import NaverWebtoon

# 통신 및 정규식, 파서
import urllib, urllib2
from bs4 import BeautifulSoup
import re

from datetime import datetime

# 이미지 처리
from PIL import Image as PIL_Image
from cStringIO import StringIO
import os

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
    today = datetime.today()
    today_str = today.strftime('%Y%m%d')
    REAL_PATH = os.path.join(MEDIA_PATH, today_str, 'work', 'webtoon')
    FIELD_PATH = os.path.join(MEDIA_PATH, today_str, 'work', 'webtoon')
    
    print 'REAL_PATH :', REAL_PATH
    if not os.path.exists(REAL_PATH):
        os.makedirs(REAL_PATH)
        print 'real path created'

    print 'FIELD_PATH :', FIELD_PATH
    if not os.path.exists(FIELD_PATH):
        os.makedirs(FIELD_PATH)
        print 'field path created'

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

    work_category, work_category_created = WorkCategory.objects.get_or_create(title=u'웹툰')
    work, work_created = Work.objects.get_or_create(category=work_category, title=comic_title, description=comic_description, author=user)

    if work_created:
        print '%s is created' % ( work.title )
    else:
        print '%s is exists' % ( work.title )

    work.description = comic_description
    work.save()

    return work

# Chapter List의 구성요소인 chapter_dict의 정보로 Chapter인스턴스 생성 후 저장, 리턴
def make_chapter(chapter_dict, work, type):
    chapter_number = chapter_dict['no']
    chapter_title = chapter_dict['title']
    chapter_thumbnail = chapter_dict['thumbnail']
    chapter_date = chapter_dict['date']

    print chapter_dict

    chapter_instance, chapter_created = Chapter.objects.get_or_create(reg_no=chapter_number, work=work)
    if not chapter_created:
        print 'Chapter (reg_no:%s) is already exists!' % ( chapter_number )
    else:
        print 'Chapter (reg_no:%s) created' % ( chapter_number )
        # ImageField에 저장될 thumbnail이름
        filename = u'%s_%s_thumbnail.jpg' % ( work.id, chapter_number )
        fieldpath = get_field_path(filename)
        # 다운로드 받을 전체 경로(MEDIA_PATH포함)
        filepath = get_save_path(filename)
        with open(filepath, 'wb') as stream:
            stream.write(chapter_thumbnail.read())
        cchapter_thumbnail.close()

        setattr(chapter_instance, 'reg_no', chapter_number)
        setattr(chapter_instance, 'work', work)
        setattr(chapter_instance, 'title', chapter_title)
        setattr(chapter_instance, 'created', chapter_date)
        setattr(chapter_instance, 'thumbnail', fieldpath)
        chapter_instance.save()

        print 'Chapter (reg_no:%s) end create' % (chapter_number)
    return chapter_instance, chapter_created

def save_chapter_contents(chapter_instance, work, images, type):
    chapter_number = chapter_instance.reg_no
    crop_list = get_croplist(images)

    # 크롭된 이미지 저장 후 Content instance 생성
    for i, image in enumerate(crop_list):
        filename = u'%s_%s_%02d_%02d.jpg' % ( work.id, chapter_number, 0, i + 1 )
        fieldpath = get_field_path(filename)
        filepath = get_save_path(filename)
        
        image.save(filepath, 'JPEG', quality=90)

        image_instance = Image(chapter=chapter_instance, sequence=i, image=fieldpath)
        image_instance.save()

def get_croplist(images):
    combined_image = None
    image_list, crop_list = [], []
    image_width, image_height = 0, []
    # StringIO 에 담겨져있는 이미지를 PIL 이미지로 바꿔서 리스트에 저장
    for i, image in enumerate(images):
        try:
            img = PIL_Image.open(images[i])
        except Exception, e:
            pass

        if img.mode != 'RGB':
            img = img.convert('RGB')

        image_list.append(img)
        image_width = img.size[0]
        image_height.append(img.size[1])

    # 이미지를 하나로 합치기 위해서 전체 사이즈에 맞는 빈 이미지 생성
    combined_image = PIL_Image.new('RGB', ( image_width, sum(image_height) ))
    # 이미지 붙이기
    for i, image in enumerate(image_list):
        y = 0 if i == 0 else sum(image_height[:i])
        combined_image.paste(image, ( 0, y, image_width, y + image_height[i] ))

    # 이미지 자르기(every 2000px)
    while combined_image.size[1] > 0:
        if combined_image.size[1] > 2000:
            crop_height = 2000
        else:
            crop_height = combined_image.size[1]

        box1 = ( 0, 0, combined_image.size[0], crop_height )
        crop_list.append(combined_image.crop(box1))

        box2 = ( 0, crop_height, combined_image.size[0], combined_image.size[1] )
        combined_image = combined_image.crop(box2)

    return crop_list

# 웹툰 크롤링
# TYPE: ChapterQueue.NAVER, ChapterQueue.DAUM
# crawl(type=ChapterQueue.TYPE, comic_number=i32, user=User): 크롤되지 않은 모든 웹툰을 크롤링함
# crawl(type=ChapterQueue.TYPE, comic_number=i32, chapter_number=i32, user=User): 한 화만 선택헤서 크롤링함
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
    if args_len == 3: # 크롤되지 않은 모든 웹툰 크롤링
        # Chapter List 가져오기
        if type == ChapterQueue.NAVER:
            chapter_list = NaverWebtoon().list(comic_number)
        elif type == ChapterQueue.DAUM:
            chapter_list = DaumLeaguetoon.list(comic_number)

        last_result = False
        for chapter in chapter_list:
            if not Chapter.filter(reg_no=chapter['no'], work=work).exists():
                last_result = crawl(type=type, comic_number=comic_number, chapter_number=chapter_list['no'], user=user)
        
        return last_result
    elif args_len == 4: # 한 화만 선택해서 크롤링
        chapter_number = kargs['chapter_number']
        # Chapter Dictionary(detail) 가져오기
        if type == ChapterQueue.NAVER:
            chapter_dict = NaverWebtoon().detail(comic_number, chapter_number)
        elif type == ChapterQueue.DAUM:
            chapter_dict = DaumLeaguetoon.detail(chapter_number)

        # Chapter 생성
        cur_chapter, chapter_created = make_chapter(chapter_dict, work, type)
        if chapter_created:
            print 'success'
            save_chapter_contents(cur_chapter, work, chapter_dict['images'], type)
            return True
        else:
            print 'Chapter not created.'
            return False
