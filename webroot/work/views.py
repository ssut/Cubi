from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect

from cubi.settings import MEDIA_URL
from work.models import *

def mobile(request, work_id, chapter_id):
    work = Work.objects.get(id=work_id)
    chapter = Chapter.objects.get(work=work, id=chapter_id)
    images = Image.objects.filter(chapter=chapter)
    print images
    contents = Content.objects.filter(chapter=chapter)
    print contents

    d = {
        'images': images,
        'media_url': MEDIA_URL,
    }

    return render_to_response('mobile/chapter.html', d)