#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

TYPE_GENDER_CHOICES = (
    ('M', '남자'),
    ('F', '여자'),
)

TYPE_MEMBER_CHOICES = (
    ('1', '독자'),
    ('2', '작가'),
)

class CubiUserManager(BaseUserManager):
    def create_user(self, type, username, first_name, last_name, email, gender, tel, access_token, password=None):
        user = self.model(
            type=type,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            tel=tel,
            access_token=access_token,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, type='2', first_name='Admin', last_name='Cubi', email='Cubi@Cubi.in', gender='M', tel='000', access_token='000', ):
        user = self.create_user(type=type, username=username, first_name=first_name, last_name=last_name, email=email, gender=gender, tel=tel, access_token=access_token, password=password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class CubiUser(AbstractUser):
    # 이미 있는 것
    # username, first_name, last_name, email,
    # password, groups, user_permissions,
    # is_staff, is_active, is_superuser,
    # last_login, date_joined
    type = models.CharField("회원 타입", max_length=1, choices=TYPE_MEMBER_CHOICES, db_index=True)
    nickname = models.CharField("닉네임", max_length=8)
    gender = models.CharField("성별", max_length=1, choices=TYPE_GENDER_CHOICES, blank=True)
    tel = models.CharField("연락처", max_length=14, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    access_token = models.CharField("페이스북 엑세스 토큰", max_length=255, blank=True)

    # 즐겨찾기, ManyToMany로 연결
    favorites = models.ManyToManyField('work.Work', related_name='user_by_favorites')
    # 자신의 작품, ManyToMany로 연결
    own_works = models.ManyToManyField('work.Work', related_name='user_by_own_works')

    objects = CubiUserManager()

    def __unicode__(self):
        return u'%s%s' % (self.last_name, self.first_name)

    def add_favorite(self, work_instance):
        self.favorites.add(work_instance)

    def add_work(self, work_instance):
        self.own_works.add(work_instance)

    def remove_favorite(self, work_instance):
        self.favorites.remove(work_instance)

    def remove_work(self, work_instance):
        self.own_works.remove(work_instance)