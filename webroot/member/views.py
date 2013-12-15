#-*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from .models import CubiUser

