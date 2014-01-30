from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

from cubi.settings import MEDIA_URL
from work.models import *

def chapter_list(request, work_id):
    work = Work.objects.get(id=work_id)
    chapters = Chapter.objects.filter(work=work).order_by('-created')