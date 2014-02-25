#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from member.models import *

class CubiUserSignupForm(forms.Form):
    email = forms.EmailField()
    nickname = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())