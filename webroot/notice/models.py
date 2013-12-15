#-*- coding: utf-8 -*-

from django.db import models

class Notice(models.Model):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    post_at = models.DateTimeField("글쓴 시간", db_index=True)
    post_href = models.CharField("링크", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = NoticeManager()

    def __unicode__(self):
        return self.title