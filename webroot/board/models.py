# -*- coding: utf-8 -*-
from django.db import models

class Notice(models.Model):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    created = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)

    def __unicode__(self):
        return self.title
