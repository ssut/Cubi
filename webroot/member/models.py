# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import utc

from tinicube.functions import day_to_string, minute_to_string
from tinicube.functions import imageinfo

from author.models import AuthorInfo


TYPE_GENDER_CHOICES = (
    ('M', '남자'),
    ('F', '여자'),
)

TYPE_MEMBER_CHOICES = (
    ('1', '독자'),
    ('2', '작가'),
)

class TinicubeUserManager(BaseUserManager):
    def create_default_user(self, username, nickname, password, type='2',
                            first_name='Admin', last_name='Cubi',
                            email='Cubi@Cubi.in', gender='M', tel='000',
                            access_token='000'):
        user = self.create_user(
            type=type, username=username, first_name=first_name,
            last_name=last_name, email=email, gender=gender, tel=tel,
            access_token=access_token, password=password)
        return user

    def create_user(self, type, username, first_name, last_name, email,
                    gender, tel, access_token, nickname="없음", password=None):
        user = self.model(
            type=type,
            username=username,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            email=email,
            gender=gender,
            tel=tel,
            access_token=access_token,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, username, type='2',
                         first_name='Admin', last_name='Cubi', gender='M',
                         tel='000', access_token='000'):
        user = self.create_user(
            type=type, username=email, first_name=first_name,
            last_name=last_name, email=email, gender=gender, tel=tel,
            access_token=access_token, password=password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class TinicubeUser(AbstractUser):
    # 이미 있는 것
    # username, first_name, last_name, email,
    # password, groups, user_permissions,
    # is_staff, is_active, is_superuser,
    # last_login, date_joined
    type = models.CharField("회원 타입", max_length=1,
                            choices=TYPE_MEMBER_CHOICES, db_index=True)
    nickname = models.CharField("닉네임", max_length=20, blank=True)
    gender = models.CharField(
        "성별", max_length=1, choices=TYPE_GENDER_CHOICES, blank=True)
    tel = models.CharField("연락처", max_length=14, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    access_token = models.CharField("페이스북 엑세스 토큰", max_length=255, blank=True)

    # 즐겨찾기, ManyToMany로 연결
    # favorites = models.ManyToManyField('work.Work',
    #               related_name='user_by_favorites', blank=True)
    # favorites = models.
    # 자신의 작품, ManyToMany로 연결
    own_works = models.ManyToManyField(
        'work.Work', related_name='user_by_own_works', blank=True)

    objects = TinicubeUserManager()

    def __unicode__(self):
        return u'%d] %s(%s)' % (self.id, self.nickname, self.email)

    def json(self):
        dict = {
            'id': self.id,
            'username': self.username,
            'name': u'%s%s' % (self.last_name, self.first_name),
            'type': self.type,
            'nickname': self.nickname,
            'gender': self.gender,
            'tel': self.tel,
            'created': minute_to_string(self.created),
        }
        if self.type == '2':
            if AuthorInfo.objects.filter(user=self).exists():
                dict['author_info'] = AuthorInfo.objects.get(user=self).json()
        return dict

    '''
    Check facebook account is connected
    '''
    @property
    def fb_connected(self):
        if self.access_token is '' or self.access_token is '000':
            return False
        elif len(self.access_token) > 10:
            return True

    '''
    Get favorites

    user = User.objects.get(id=id)
    works = user.work_favorites
    authors = user.author_favorites
    '''
    @property
    def work_favorites(self):
        favorites = UserWorkFavorites.objects.filter(user=self)
        return favorites

    @property
    def author_favorites(self):
        favorites = UserAuthorFavorites.objects.filter(user=self)
        return favorites

    @property
    def author_info(self):
        if self.type == '2':
            author_info = AuthorInfo.objects.get(user=self)
            return author_info.json()
        else:
            return ''

    def check_favorites_exist(self, inst):
        from work.models import Work
        if isinstance(inst, Work):
            print self, inst
            return UserWorkFavorites.objects.filter(
                user=self, work=inst).exists()
        elif isinstance(inst, TinicubeUser):
            return UserAuthorFavorites.objects.create(
                user=self, author=inst).exists()

        return True

    '''
    Add favorites example

    user = User.objects.get(id=id)
    work = Work.objects.get(id=work_id)
    author = User.objects.get(id=author_id)
    user.add_favorites(work)
    user.add_favorites(author)
    '''
    def add_favorites(self, inst):
        from work.models import Work
        if isinstance(inst, Work):
            favorite = UserWorkFavorites.objects.create(user=self, work=inst)
        elif isinstance(inst, TinicubeUser):
            favorite = UserAuthorFavorites.objects.create(
                user=self, author=inst)

        return favorite

    '''
    Delete favorites example

    user = User.objects.get(id)
    work = Work.objects.get(id=work_id)
    author = User.objects.get(id=author_id)
    try:
        user.delete_favorites(work)
        user.delete_favorites(author)
    except ObjectDoesNotExist, e:
        print 'favorite object does not exist'
    '''
    def delete_favorites(self, inst):
        if isinstance(inst, UserWorkFavorites):
            instance = UserWorkFavorites.objects.filter(user=self, work=inst)
        elif isinstance(inst, UserAuthorFavorites):
            instance = UserWorkFavorites.objects.filter(user=self, author=inst)

        if instance.exists():
            instance.delete()
        else:
            raise ObjectDoesNotExist()

    def add_work(self, work_instance):
        self.own_works.add(work_instance)

    def remove_work(self, work_instance):
        self.own_works.remove(work_instance)


class UserWorkFavorites(models.Model):
    from work.models import Work
    user = models.ForeignKey(
        TinicubeUser, related_name='work_favorites_by_user')
    work = models.OneToOneField(Work, related_name='work_favorites_by_work')

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.work)


class UserAuthorFavorites(models.Model):
    user = models.ForeignKey(
        TinicubeUser, related_name='author_favorites_by_user')
    author = models.ForeignKey(
        TinicubeUser, related_name='author_favorites_by_author')

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.author)
