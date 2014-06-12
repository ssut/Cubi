# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from author.models import *

CHOICES_TYPE = (
    ('webtoon_naver', u'네이버 웹툰'),
    ('webtoon_daum', u'다음 웹툰'),
)
'''
6-2-1. 웹툰 - 작품 정보 입력
- 정보
제목
장르
작품 소개 (짧은 글)
작품 번호 (http://webtoon.daum.net/league/view/8767 에서의 8767)
- 첨부파일
타이틀 이미지 - 1080x480
썸네일 이미지 - 1080x480
로딩 이미지 (선택사항) - 1080x1920
큰 아이콘 이미지 - 1024x1024또는 2048x2048
작은 아이콘 이미지 - 512x512
'''
class AddworkForm(forms.Form):
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_TYPE)
    title = forms.CharField(label='제목', max_length=100)
    genre = forms.CharField(label='장르', max_length=20)
    introduce = forms.CharField(label='작품 소개', max_length=200)
    work_num = forms.IntegerField(label='작품 번호')
    image_cover = forms.ImageField(label='타이틀 이미지')
    image_thumbnail = forms.ImageField(label='썸네일 이미지')
    image_loading = forms.ImageField(label='로딩 이미지', required=False)
    image_largeicon = forms.ImageField(label='큰 아이콘')
    image_smallicon = forms.ImageField(label='작은 아이콘')
