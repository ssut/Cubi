from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

from cubi.settings import MEDIA_URL
from work.models import *

