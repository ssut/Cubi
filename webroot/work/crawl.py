#-*- coding: utf-8 -*-
from django.conf import settings
from crawler.daum_webtoon import list as daum_list
from crawler.daum_leaguetoon import list as daum_league_list
from crawler.daum_leaguetoon import detail as daum_league_detail

# 통신 및 정규식, 파서
import urllib, urllib2
from bs4 import BeautifulSoup
import re

# 이미지처리
import Image as PIL_Image
from cStringIO import StringIO
import os

real_path = ''
field_path = ''
media_path = settings.MEDIA_ROOT

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from work.models import *
from member.models import *
'''
폴더구조
    날짜기준으로 생성
    기본 : yyyymmdd/
    Work - Webtoon : 기본/work/webtoon/
        썸네일 : (chapter_number)_thumbnail.jpg

'''
# 디렉토리 생성
def make_directory():
    global path
    today = datetime.today()
    today_str = today.strftime('%Y%m%d')
    real_path = os.path.join(media_path, today_str, 'work', 'webtoon')
    field_path = os.path.join(today_str, 'work', 'webtoon')
    
    print 'real_path :', real_path
    if not os.path.exists(real_path):
        os.makedirs(real_path)
        print 'real path created'

    print 'field_path :', field_path
    if not os.path.exists(field_path):
        os.makedirs(field_path)
        print 'field path created'

# Work생성 및 Chapter List 리턴
def get_chapter_list_and_create_work(comic_number, user):
    league_info = daum_league_list(comic_number)
    comic_title = league_info['comic_title']
    comic_author_name = league_info['comic_author_name']
    comic_description = league_info['comic_description']
    comic_genre = league_info['comic_genre']
    comic_url_img_title = league_info['comic_url_img_title']
    chapter_list = league_info['chapter_list']

    ## 임시 유저생성 & 적용 부분
    # count = User.objects.count()
    # str_count = str(count)
    # password = '123'
    # print comic_author_name
    # if User.objects.filter(nickname=comic_author_name).exists():
    #     user = User.objects.filter(nickname=comic_author_name)
    # else:
    #     user = User.objects.create_default_user(count, comic_author_name, password)
    #     user.nickname = comic_author_name
    #     user.save()

    work_category, work_category_created = WorkCategory.objects.get_or_create(title=u'웹툰')
    work, work_created = Work.objects.get_or_create(category=work_category, title=comic_title, description=comic_description, author=user)

    if work_created:
        print '%s is created' % (work.title)
    else:
        print '%s is exist' % (work.title)

    work.description = comic_description
    work.save()

    return chapter_list

# Chapter List 리턴
def get_chapter_list(comic_number):
    league_info = daum_league_list(comic_number)
    chapter_list = league_info['chapter_list']
    return chapter_list

# make_directory에서 지정된 전역변수 path를 이용, media_path를 포함한 저장할 파일명의 path를 반환
def get_save_path(filename):
    global real_path
    return os.path.join(real_path, filename)

# ImageField, FileField에 저장할 path반환
def get_field_path(filename):
    global field_path
    return os.path.join(field_path, filename)    

# Chapter List의 구성요소인 chapter_dict의 정보로 Chapter인스턴스 생성 후 저장, 리턴
def make_chapter(chapter_dict):
    chapter_number = chapter_dict['detail_num']
    chapter_title = chapter_dict['title']
    chapter_url_thumbnail = chapter_dict['url_thumbnail']
    chapter_date = chapter_dict['date']

    chapter_instance, chapter_created = Chapter.objects.get_or_create(reg_no=chapter_number)
    if chapter_created:
        print 'Chapter (reg_no:%s) is Exist!' % (chapter_number)
    else:
        print 'Chapter (reg_no:%s) start create' % (chapter_number)
        # 썸네일 저장
        url = chapter_url_thumbnail
        save_ext = '.jpg'
        # ImageField에 저장될 thumbnail이름
        filename = u'%s_thumbnail%s' % (chapter_number, ext)
        fieldpath = get_field_path(filename)
        # 다운로드 받을 전체 경로(media_path포함)
        filepath = get_save_path(filename)
        # urllib로 지정한 이름으로 이미지 다운로드 및 저장
        urllib.urlretrieve(url, filepath)

        chapter_instance = Chapter.objects.create(reg_no=chapter_number, work=work, title=chapter_title, created=chapter_date, thumbnail=fieldpath)
        chapter_instance.save()
        print 'Chapter (reg_no:%s) end create' % (chapter_number)
    return chapter_instance, chapter_created

# Chapter Number를 받아 Content(Image)생성 후 저장
def save_chapter_contents(chapter_instance):
    chapter_number = chapter_instance.chapter_number
    # Chapter의 Content 인스턴스 생성 작업
    image_list = daum_league_detail(chapter_number)
    # 이미지 저장
    for i, image in enumerate(image_list):
        image = image_list[i]
        image_name = image['name']
        image_url = image['url']
        image_order = image['order']

        # 이부분은 splittext사용
        filename, ext = os.path.splittext(image_name)
        ext = ext.lower()

        # 저장할 이미지 이름 지정
        filename = u'%s_%02d.%s' % (chapter_number, i+1, ext)
        filename2 = os.path.join('origin/', filename)
        fieldpath = get_field_path(filename2)
        filepath = get_save_path(filename2)
        print fieldpath
        print filepath
        urllib.urlretrieve(image_url, filepath)

        # 다운받은 이미지 크롭 후 크롭리스트 리턴 (get_croplist함수 사용)
        crop_list = get_croplist(filepath)
        
        # 크롭파일 저장, Content인스턴스 생성
        for j, crop_image in enumerate(crop_list):
            crop_filename = u'%s_%02d_%02d.%s' % (chapter_number, i+1, j+1, ext)
            fieldpath = get_field_path(crop_filename)
            filepath = get_save_path(crop_filename)

            crop_image.save(filepath, ext, quality=90)

            image_instance = Image(chapter=chapter_instance, sequence=j, image=fieldpath)
            image_instance.save()

# 이미지 열어 크롭 후 크롭리스트 리턴
def get_croplist(filepath):
    try:
        im = PIL_Image.open(filepath)
    except:
        continue

    # P모드에서는 작업 불가
    if im.mode != 'RGB':
        im = im.convert('RGB')

    print 'FileName : ' + filename + ' (' + str(im.size[0]) + ', ' + str(im.size[1]) + ')'

    # 세로크기 4000px씩 Crop후 crop_list에 추가
    print 'Crop Start'
    crop_list = []
    while im.size[1] > 0:
        if im.size[1] > 2000:
            crop_height = 2000
        else:
            crop_height = im.size[1]

        box1 = (0, 0, im.size[0], crop_height)
        crop_list.append(im.crop(box1))

        box2 = (0, crop_height, im.size[0], im.size[1])
        im = im.crop(box2)

        print '    ' + str(im.size[1])
    print 'Crop End'
    return crop_list


# 다음 리그 크롤링
def crawl_daumleague(comic_number, user):
    # 디렉토리 생성
    make_directory()
    # Work생성, ChapterList 받아오기
    chapter_list = get_chapter_list_and_create_work()
    # ChapterList의 ChapterDict별로 Chapter생성
    for chapter_dict in chapter_list:
        cur_chapter, chapter_created = make_chapter(chapter_dict)
        if chapter_created:
            # 생성한 ChapterInstance에 Content(Image) Instance 생성 후 저장
            save_chapter_contents(cur_chapter)
        else:
            pass


# 정식웹툰
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