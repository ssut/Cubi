#-*- coding: utf-8 -*-
from django.db import models

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from cubi.functions import minute_to_string

class WaitConvert(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s (%s)' % (self.user.nickname, self.user.email, minute_to_string(self.created))

    def convert(self):
        self.user.type = '2'
        self.user.save()

class AuthorInfo(models.Model):
    user = models.ForeignKey(User, related_name='authorinfo_by_user')
    profile_image = models.ImageField('작가 프로필 이미지', upload_to='author/', blank=True)
    nickname = models.CharField('작가 닉네임', max_length=30)
    introduce_simple = models.CharField('작가 한줄소개', max_length=200, blank=True)
    introduce_full = models.TextField('작가 소개', blank=True)
    verified = models.BooleanField('민증사본,통장사본 검증여부', default=False)

    def __unicode__(self):
        return u'%s%s\'s AuthorInfo' % (self.user.last_name, self.user.first_name)
