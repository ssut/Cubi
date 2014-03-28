#-*- coding: utf-8 -*-
import os
from django.db import models

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from cubi.functions import day_to_string, minute_to_string, time_to_string
from cubi.functions import imageinfo, imageinfo2

# Upload path
path_image = 'image/'
path_image_work = os.path.join(path_image, 'work')

path_image_chapter = os.path.join(path_image, 'chapter')
path_image_chapter_cover = os.path.join(path_image_chapter, 'cover')
path_image_chapter_thumbnail = os.path.join(path_image_chapter, 'thumbnail')

path_image_content = os.path.join(path_image, 'content')

# Dynamic upload path
def get_work_cover_path(work_instance, filename):
    path = '%s'
def get_work_thumbnail_path(work_instance, filename):
    path = '%s'

def get_image_chapter_cover_path(chapter_instance, filename):
    path1 = os.path.join(path_image_chapter_cover, str(chapter_instance.work.id))
    path2 = os.path.join(path1, filename)
    return path2

def get_image_chapter_thumbnail_path(chapter_instance, filename):
    path1 = os.path.join(path_image_chapter_thumbnail, str(chapter_instance.work.id))
    path2 = os.path.join(path1, filename)
    return path2

def get_image_content_path(content_instance, filename):
    path1 = os.path.join(path_image_content, str(content_instance.chapter.work.id))
    path2 = os.path.join(path1, str(content_instance.chapter.id))
    path3 = os.path.join(path2, filename)
    return path3

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

# 공통적으로 사용할 댓글 클래스
class Comment(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s%s Comment(%s)' % (self.author.last_name, self.author.first_name, self.created)

    def json(self):
        return {
            'id': self.id,
            'author': self.author.json(),
            'content': self.content,
            'created_date': day_to_string(self.created),
            'created_time': time_to_string(self.created),
        }

# 공통적으로 사용할 평점 클래스
CHOICES_RATING = [(i,i+1) for i in range(10)]
class Rating(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(choices=CHOICES_RATING)

    def __unicode__(self):
        return u'%s%s Rating(%d)' % (self.author.last_name, self.author.first_name, self.score)

    def json(self):
        return {
            'id': self.id,
            'author': self.author.json(),
            'created_date': day_to_string(self.created),
            'created_time': time_to_string(self.created),
            'score': self.score,
        }


'''
- 구조 -
Work(작품)
    Chapter(각 화)
        Content(내용)
            Comic, Text, Comic.... Content의 Sequence순으로 배열
    Chapter(각 화)
        Content(내용)
            Comic, Text, Comic.... Content의 Sequence순으로 배열
'''
# 작품 카테고리
class WorkCategory(models.Model):
    title = models.CharField(max_length=100)
    def __unicode__(self):
        return self.title

# 작품
class Work(models.Model):
    category = models.ForeignKey(WorkCategory)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    market_android = models.CharField(max_length=100, blank=True)
    market_ios = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=path_image_work, blank=True)
    cover = models.ImageField(upload_to=path_image_work, blank=True)
    image_loading = models.ImageField(upload_to=path_image_work, blank=True)
    image_largeicon = models.ImageField(upload_to=path_image_work, blank=True)
    image_smallicon = models.ImageField(upload_to=path_image_work, blank=True)

    def __unicode__(self):
        return self.title

    def json(self):
        return {
            'id': self.id,
            'category': self.category.title,
            'author': self.author.nickname,
            'title': self.title,
            'description': self.description,
            'market_android': self.market_android,
            'market_ios': self.market_ios,
            'created': day_to_string(self.created),
            'thumbnail': imageinfo(self.thumbnail),
            'cover': imageinfo2(self.cover),
            'image_loading': imageinfo(self.image_loading),
            'image_largeicon': imageinfo(self.image_largeicon),
            'image_smallicon': imageinfo(self.image_smallicon),
        }

# 작품 댓글
class WorkComment(Comment):
    work = models.ForeignKey(Work)
    
    def __unicode__(self):
        return u'%s%s - %s Comment' % (self.author.last_name, self.author.first_name, self.work.title)

    def json(self):
        parent_dict = self.comment_ptr.json()
        cur_dict = {
            'work': self.work.json(),
        }
        combine_dict = dict(parent_dict.items() + cur_dict.items())
        return combine_dict

# 챕터(각 작품의 1,2,3화....)
class Chapter(models.Model):
    reg_no = models.IntegerField()
    work = models.ForeignKey(Work)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=get_image_chapter_thumbnail_path, blank=True)
    cover = models.ImageField(upload_to=get_image_chapter_cover_path, blank=True)

    def __unicode__(self):
        return self.title

    def json(self):
        return {
            'id': self.id,
            'reg_no': self.reg_no,
            'title': self.title,
            'created': day_to_string(self.created),
            'thumbnail': imageinfo(self.thumbnail),
            'cover': imageinfo(self.cover),
        }

# 챕터 댓글
class ChapterComment(Comment):
    chapter = models.ForeignKey(Chapter)

    def __unicode__(self):
        return u'%s%s - %s Comment' % (self.author.last_name, self.author.first_name, self.chapter.title)

    def json(self):
        parent_dict = self.comment_ptr.json()
        cur_dict = {
            'chapter': self.chapter.json(),
        }
        combine_dict = dict(parent_dict.items() + cur_dict.items())
        return combine_dict

# 챕터 평점
class ChapterRating(Rating):
    chapter = models.ForeignKey(Chapter)

    def __unicode__(self):
        return u'%s%s - %s Rating(%d)' % (self.author.last_name, self.author.first_name, self.chapter.title, self.score)

    def json(self):
        parent_dict = self.rating_ptr.json()
        cur_dict = {
            'chapter': self.chapter.json(),
        }
        combine_dict = dict(parent_dict.items() + cur_dict.items())
        return combine_dict

# 셀러리 큐
# --------
# target = ChapterQueue.NAVER or ChapterQueue.DAUM
# comic_number = 웹툰 사이트에서의 웹툰 고유번호
# chapter_number = 웹툰 사이트에서의 각 챕터 고유번호, -1 로 입력하면 모두 크롤링함
# is_checked = celery task 가 실행됐는지 여부
# checked_at = celery task 가 실행된 시간
# is_succeeded = 크롤링에 성공했는지에 대한 여부
class ChapterQueue(models.Model):
    NAVER = 'NAVER'
    DAUM = 'DAUM'
    TARGET_CHOICES = (
        (NAVER, u'네이버'),
        (DAUM, u'다음'),
    )
    target = models.CharField(max_length=10, choices=TARGET_CHOICES)
    user = models.ForeignKey(User)
    comic_number = models.IntegerField()
    chapter_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_checked = models.BooleanField(default=False)
    checked_at = models.DateTimeField(blank=True)
    is_succeeded = models.BooleanField(default=False)

# 주기적으로 실행될 셀러리 큐
# --------
# target = ChapterQueue.NAVER or ChapterQueue.DAUM
# comic_number = 웹툰 사이트에서의 웹툰 고유번호
# every_hour = 매일 몇시에 크롤링할지에 대한 시간정보
# last_run_at = 마지막으로 크롤링이 실행된 시간
# last_run_result = 마지막 크롤링 성공 여부
class ChapterPeriodicQueue(models.Model):
    target = models.CharField(max_length=10, choices=ChapterQueue.TARGET_CHOICES)
    user = models.ForeignKey(User)
    comic_number = models.IntegerField()
    every_hour = IntegerRangeField(min_value=0, max_value=23, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_run_at = models.DateTimeField(blank=True)
    last_run_result = models.BooleanField(default=False)


'''
내용(Content)
    이미지 : Image
    글 : Text
    링크 : 어떻게 구현할지 고민(Text에 링크속성?)
    추후 추가 가능
'''
class Content(models.Model):
    chapter = models.ForeignKey(Chapter)
    sequence = models.IntegerField(default=0)
    def __unicode__(self):
        return u'%s - %s (%d)' % (self.chapter.work.title, self.chapter.title, self.sequence)

class Image(Content):
    image = models.ImageField(upload_to=get_image_content_path)
    def __unicode__(self):
        return u'%s - %s (Image, %d)' % (self.chapter.work.title, self.chapter.title, self.sequence)

class Text(Content):
    text = models.TextField(blank=True)
    def __unicode__(self):
        return u'%s - %s (Text, %d)' % (self.chapter.work.title, self.chapter.title, self.sequence)
