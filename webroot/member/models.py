#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseuser, BaseUserManager

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

    objects = CubiUserManager()

    def __unicode__(self):
        return u'%s%s' % (self.last_name, self.first_name)
