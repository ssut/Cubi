# -*- coding: utf-8 -*-
import os

from datetime import datetime

from django.db import models

from tinicube.functions import day_to_string, minute_to_string, time_to_string
from tinicube.functions import imageinfo
from tinicube.settings import MEDIA_URL

from member.models import TinicubeUser as User

# Upload path
def get_path(instance, filename):
    today = datetime.today()
    today_str = today.strftime('%Y%m%d')

    path = os.path.join(today_str, filename)
    return path


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None,
                 max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'min_value': self.min_value,
            'max_value': self.max_value
        }
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

# 공통적으로 사용할 댓글 클래스
class Comment(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s%s Comment(%s)' % (
            self.author.last_name, self.author.first_name, self.created)

    def json(self):
        return {
            'id': self.id,
            'author': self.author.json(),
            'content': self.content,
            'created_date': day_to_string(self.created),
            'created_time': time_to_string(self.created),
        }

# 공통적으로 사용할 평점 클래스
class Rating(models.Model):
    # generate choices: tuple([(i, (i / 2.0)) for i in range(1, 11)])
    RATING_CHOICES = (
        (1, 1), (2, 2),
        (3, 3), (4, 4),
        (5, 5), (6, 6),
        (7, 7), (8, 8),
        (9, 9), (10, 10)
    )
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(choices=RATING_CHOICES)

    def __unicode__(self):
        return u'%s%s Rating(%d)' % (
            self.author.last_name, self.author.first_name, self.score)

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
    work_num = models.IntegerField(blank=True, null=True)
    work_target = models.CharField(max_length=10, blank=True)
    category = models.ForeignKey(WorkCategory)
    author = models.ForeignKey(User)
    title = models.CharField('작품명', max_length=200)
    description_simple = models.CharField('작품 한줄 설명', max_length=100)
    description_full = models.TextField('작품 설명', blank=True)
    market_android = models.CharField(
        '안드로이드 마켓 주소', max_length=100, blank=True)
    market_ios = models.CharField('iOS 마켓 주소', max_length=100, blank=True)
    created = models.DateTimeField('생성일자', auto_now_add=True)

    '''
    image_thumbnail_square
        작품 썸네일 (정사각형)        [400x400]
    image_thumbnail_rectangle
        작품 썸네일 (배너형)          [440x120]
    image_cover_large
        전체 작품 목록 쇼케이스        [900x345]
    image_cover
        전체 작품 목록 배너형 썸네일    [290x145]

    mobile_cover_top
        모바일 ChapterList 커버이미지   [1080x714]
    mobile_cover_pager
        모바일 통합 앱 CoverPager 이미지 [1080x714, 제목 및 설명 글자 포함]
    mobile_cover_small
        모바일 통합 앱 커버이미지         [1080x240]

    mobile_loading_android, mobile_loading_ios
        모바일 로딩 이미지
    mobile_largeicon, mobile_smalliocn
        모바일 아이콘 이미지
    '''
    image_thumbnail_square = models.ImageField('정사각형 썸네일',
                                               upload_to=get_path, blank=True)
    image_thumbnail_rectangle = models.ImageField(
        '배너형태 썸네일', upload_to=get_path, blank=True)
    image_cover_large = models.ImageField(
        'WorkList상단 돌아가는 큰 이미지 [900x345]', upload_to=get_path, blank=True)
    image_cover = models.ImageField(
        'WorkList각 작품의 Cover [400x200]', upload_to=get_path, blank=True)

    mobile_cover_top = models.ImageField(
        '모바일 챕터 리스트 상단 이미지 [1080x480]', upload_to=get_path, blank=True)
    mobile_cover_pager = models.ImageField(
        '모바일 챕터 리스트 상단 이미지 [1080x480] 제목 및 설명 포함',
        upload_to=get_path, blank=True)
    mobile_cover_small = models.ImageField(
        '통합앱 메인화면 커버이미지(1080x240)', upload_to=get_path, blank=True)
    mobile_loading_android = models.ImageField(
        '안드로이드 로딩 이미지', upload_to=get_path, blank=True)
    mobile_loading_ios = models.ImageField(
        'iOS 로딩 이미지', upload_to=get_path, blank=True)
    mobile_largeicon = models.ImageField(
        '모바일 큰 아이콘(1024x1024 이상)', upload_to=get_path, blank=True)
    mobile_smallicon = models.ImageField(
        '모바일 작은 아이콘(안드144x144, iOS)', upload_to=get_path, blank=True)

    last_upload = models.DateField('마지막 챕터 업데이트 날짜', blank=True, null=True)
    chapter_count = models.IntegerField('챕터 수', blank=True, null=True)

    @property
    def chapters_manager(self):
        return self.chapter_by_work

    @property
    def chapters(self):
        return self.chapters_manager.all()

    @property
    def mobile_cover_url(self):
        if self.mobile_cover_small:
            return self.mobile_cover_small.url
        else:
            return '/static/img/_.no.image.png'

    @property
    def cover_url(self):
        if self.image_cover:
            return self.image_cover.url
        else:
            return '/static/img/_.no.image.png'

    @property
    def thumbnail_url(self):
        if self.image_cover:
            return self.image_cover.url
        else:
            return '/static/img/_.no.image.png'
        # chapters = Chapter.objects.filter(work=self).order_by('-reg_no')
        # if len(chapters) > 0:
        #     if chapters[0].thumbnail:
        #         chapter = chapters[0]
        #         return chapter.thumbnail.url
        #     else:
        #         return '/static/img/_.no.image.png'
        # else:
        #     return '/static/img/_.no.image.png'

    @property
    def avg_rating(self):
        dict = {}
        ratings = ChapterRating.objects.filter(chapter__work=self)
        avg_rating = ratings.aggregate(models.Avg('score'))['score__avg']
        if avg_rating:
            dict['rating'] = round(avg_rating / 2.0, 1)
            dict['count'] = ratings.count()
        else:
            dict['rating'] = 0.0
            dict['count'] = 0

        return dict

    def __unicode__(self):
        return self.title

    def json(self):
        return {
            'id': self.id,
            'category': self.category.title,
            'author': self.author.nickname,
            'title': self.title,
            'avg_rating': self.avg_rating,
            'description_simple': self.description_simple,
            'description_full': self.description_full,
            'market_android': self.market_android,
            'market_ios': self.market_ios,
            'created': day_to_string(self.created),

            'image_thumbnail_square': imageinfo(self.image_thumbnail_square),
            'image_thumbnail_rectangle':
                imageinfo(self.image_thumbnail_rectangle),
            'image_cover_large': imageinfo(self.image_cover_large),
            'image_cover': imageinfo(self.image_cover),

            'mobile_cover_top': imageinfo(self.mobile_cover_top),
            'mobile_cover_pager': imageinfo(self.mobile_cover_pager),
            'mobile_cover_small': imageinfo(self.mobile_cover_small),
            'mobile_loading_android': imageinfo(self.mobile_loading_android),
            'mobile_loading_ios': imageinfo(self.mobile_loading_ios),
            'mobile_largeicon': imageinfo(self.mobile_largeicon),
            'mobile_smallicon': imageinfo(self.mobile_smallicon),

            'last_upload': day_to_string(self.last_upload),
            'chapter_count': self.chapter_count,
        }

# 작품 댓글
class WorkComment(Comment):
    work = models.ForeignKey(Work)

    def __unicode__(self):
        return u'%s%s - %s Comment' % (
            self.author.last_name, self.author.first_name, self.work.title)

    def json(self):
        parent_dict = self.comment_ptr.json()
        cur_dict = {
            'work': self.work.json(),
        }
        combine_dict = dict(parent_dict.items() + cur_dict.items())
        return combine_dict

# 챕터(각 작품의 1,2,3화....)
class Chapter(models.Model):
    '''
    thumbnail
        챕터 썸네일      [400x235]

    챕터 썸네일 외에는 선택사항
    thumbnail_large
        더 큰 썸네일      [800x470]
    cover
        챕터 커버 이미지   [600x350]
    cover_large
        더 큰 커버       [1200x700]
    '''
    reg_no = models.IntegerField()
    work = models.ForeignKey(Work, related_name='chapter_by_work')
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=get_path, blank=True)
    thumbnail_large = models.ImageField(upload_to=get_path, blank=True)
    cover = models.ImageField(upload_to=get_path, blank=True)
    cover_large = models.ImageField(upload_to=get_path, blank=True)
    public = models.BooleanField(default=True)
    description = models.TextField(blank=True, max_length=150)

    @property
    def avg_rating(self):
        try:
            if self._avg_rating:
                return self._avg_rating
        except:
            self._avg_rating = {}

        dict = {}
        ratings = ChapterRating.objects.filter(chapter=self)
        avg_rating = ratings.aggregate(models.Avg('score'))['score__avg']
        if avg_rating:
            dict['avg_rating'] = avg_rating
            dict['count'] = ratings.count()

            tmp_rating = rating = avg_rating / 2
            rating_str = u''
            for i in range(int(rating)):
                rating_str += u'●'
                tmp_rating -= 1
            if tmp_rating > 0:
                rating_str += u'◐'
            for i in range(5 - len(rating_str)):
                rating_str += u'○'

            dict['rating_str'] = rating_str
        else:
            dict['avg_rating'] = 0.0
            dict['count'] = 0
            dict['rating_str'] = u'○○○○○'
        self._avg_rating = dict
        return dict

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return '/static/img/_.no.image.png'

    @property
    def comment_count(self):
        return ChapterComment.objects.filter(chapter=self).count()

    def __unicode__(self):
        return self.title

    def json(self):
        return {
            'work_title': self.work.title,
            'work_author': self.work.author.nickname,
            'work_id': self.work.id,
            'id': self.id,
            'avg_rating': self.avg_rating,
            'reg_no': self.reg_no,
            'title': self.title,
            'created': day_to_string(self.created),
            'thumbnail': imageinfo(self.thumbnail),
            'thumbnail_large': imageinfo(self.thumbnail_large),
            'cover': imageinfo(self.cover),
            'cover_large': imageinfo(self.cover_large),
            'public': self.public,
            'description': self.description,
            'comment_count': self.comment_count,
        }

    def save(self, *args, **kwargs):
        super(Chapter, self).save(*args, **kwargs)
        self.work.chapter_count = self.work.chapter_by_work.count()
        self.work.last_upload = self.work.chapter_by_work.order_by('-created') \
            .first().created
        self.work.save()


# 챕터 댓글
class ChapterComment(Comment):
    chapter = models.ForeignKey(Chapter)

    def __unicode__(self):
        return u'%s%s - %s Comment' % (
            self.author.last_name, self.author.first_name, self.chapter.title)

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
        return u'%s%s - %s Rating(%d)' % (
            self.author.last_name, self.author.first_name,
            self.chapter.title, self.score)

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
    checked_at = models.DateTimeField(blank=True, null=True)
    is_succeeded = models.BooleanField(default=False)

# 주기적으로 실행될 셀러리 큐
# --------
# target = ChapterQueue.NAVER or ChapterQueue.DAUM
# comic_number = 웹툰 사이트에서의 웹툰 고유번호
# every_hour = 매일 몇시에 크롤링할지에 대한 시간정보
# last_run_at = 마지막으로 크롤링이 실행된 시간
# last_run_result = 마지막 크롤링 성공 여부
# enabled = 켤지 끌지
class ChapterPeriodicQueue(models.Model):
    target = models.CharField(
        max_length=10, choices=ChapterQueue.TARGET_CHOICES)
    user = models.ForeignKey(User)
    comic_number = models.IntegerField()
    every_hour = IntegerRangeField(min_value=0, max_value=23, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_run_at = models.DateTimeField(blank=True)
    last_run_result = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

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
        return u'%s - %s (%d)' % (
            self.chapter.work.title, self.chapter.title, self.sequence)

class Image(Content):
    image = models.ImageField(upload_to=get_path)

    def __unicode__(self):
        return u'%s - %s (Image, %d)' % (
            self.chapter.work.title, self.chapter.title, self.sequence)

class Text(Content):
    text = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s - %s (Text, %d)' % (
            self.chapter.work.title, self.chapter.title, self.sequence)
