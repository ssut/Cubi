#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from member.models import *
from member.widgets import SplitInputWidget

class CubiUserSignupForm(forms.Form):
    email = forms.EmailField()
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class CubiUserSigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class CubiUserConvertToAuthorForm(forms.Form):
    work_name = forms.CharField(label='작품 이름', max_length=100)
    work_url = forms.URLField(label='작품 주소 링크')
    last_name = forms.CharField(label='성', max_length=20)
    first_name = forms.CharField(label='이름', max_length=20)
    phone_number = forms.CharField(
        label='휴대전화 번호',
        max_length=14,
        widget=SplitInputWidget(
            number=3,
            each_attrs=[
                {'class': 'input-mini', 'maxlength': '4'},
                {'class': 'input-mini', 'maxlength': '4'},
                {'class': 'input-mini', 'maxlength': '4'},
            ],
        )
    )

class CubiUserEditForm(forms.Form):
    email = forms.EmailField()
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class CubiUserPasswordChangeForm(forms.Form):
    original_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password_confirm = forms.CharField(widget=forms.PasswordInput())