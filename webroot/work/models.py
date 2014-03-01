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
path_image_work_cover = os.path.join(path_image_work, 'cover')
path_image_work_thumbnail = os.path.join(path_image_work, 'thumbnail')

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
    thumbnail = models.ImageField(upload_to=path_image_work_thumbnail, blank=True)
    cover = models.ImageField(upload_to=path_image_work_cover, blank=True)

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
    reg_no = models.CharField(blank=True, max_length=100)
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
