#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from member.models import *

class CubiUserSignupForm(forms.Form):
    email = forms.EmailField()
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class CubiUserSigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class CubiUserConvertToAuthorForm(forms.Form):
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)