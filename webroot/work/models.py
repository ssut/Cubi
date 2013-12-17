#-*- coding: utf-8 -*-
import os
from django.db import models

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

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
# 작품
class Work(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=path_image_work_thumbnail)
    cover = models.ImageField(upload_to=path_image_work_cover)

    def __unicode__(self):
        return self.title

# 챕터(각 작품의 1,2,3화....)
class Chapter(models.Model):
    work = models.ForeignKey(Work)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=get_image_chapter_thumbnail_path)
    cover = models.ImageField(upload_to=get_image_chapter_cover_path)

    def __unicode__(self):
        return self.title


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