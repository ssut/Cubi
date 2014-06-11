# -*- coding: utf-8 -*-
from django.db import models

from tinicube.functions import imageinfo
from tinicube.functions import minute_to_string
from tinicube.settings import DEFAULT_PROFILE_IMAGE

class AuthorInfo(models.Model):
    user = models.ForeignKey(
        'member.TinicubeUser', related_name='authorinfo_by_user')
    profile_image = models.ImageField(
        '작가 프로필 이미지', upload_to='author/', blank=True)
    nickname = models.CharField('작가 닉네임', max_length=30)
    introduce_simple = models.CharField('작가 한줄소개', max_length=200, blank=True)
    introduce_full = models.TextField('작가 소개', blank=True)
    verified = models.BooleanField('민증사본,통장사본 검증여부', default=False)

    def __unicode__(self):
        return u'%s%s\'s AuthorInfo' % (
            self.user.last_name, self.user.first_name)

    def json(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'introduce_simple': self.introduce_simple,
            'introduce_full': self.introduce_full,
            'verified': self.verified,
            'profile_image': imageinfo(self.profile_image,
                                       DEFAULT_PROFILE_IMAGE),
        }
