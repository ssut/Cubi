from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

import json

from cubi.settings import MEDIA_URL
from work.models import *

def list(request, work_id):
    work = Work.objects.get(id=work_id)
    chapters = Chapter.objects.filter(work=work).order_by('-created')

    data = {
        'work': work.json(),
        'chapters': [chapter.json() for chapter in chapters],
    }

    return HttpResponse(json.dumps(data), content_type="application/json")