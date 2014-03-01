#-*- coding: utf-8 -*-
from django.test import TestCase

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.test.client import Client
import random

from member.models import *
from work.models import *
from work.crawl import crawl_daumleague
import sys, os

class Crawl(TestCase):
    def daumleague(self):
        user = CubiUser.objects.get(id=1)
        comic_number = '1549'

        crawl_daumleague(comic_number, user)


class WorkTest(TestCase):
    def setUp(self):
        # setup commenter ( 100 user )
        commenters = []
        for x in range(1,30):
            commenter_str = "commenter_" + str(x)
            commenter = User.objects.create_default_user(commenter_str,
                    commenter_str, commenter_str, type="1")
            commenters.append(commenter)
        # setup author ( user )
        author = User.objects.create_default_user("author1","author1","author1")
        #(self, username, nickname, password, type='2', first_name='Admin', last_name='Cubi', email='Cubi@Cubi.in', gender='M', tel='000', access_token='000'):
        # setup category
        category = WorkCategory(title="test category")
        category.save()
        # create work
        # prepare thumbail, conver file
        work = Work(
                category = category,
                author = author,
                title = "test work",
                description = "test description",
                market_android = "market android",
                market_ios = "market ios")
        work.save()
        # create work comment
        for x in range(1,random.randrange(2,100)):
            rand_id = random.randrange(2,29)
            commenter = commenters[rand_id]
            wc = WorkComment(
                    work = work,
                    author = commenter,
                    content = "%i 번째 댓글" % x )
            wc.save()
        # create chapter
        for chapter_id in range(1,10):
            c = Chapter(
                    reg_no = "%i 화" % chapter_id,
                    work = work,
                    title = "%i 화 타이틀 " % chapter_id)
            c.save()
            for x in range(1,random.randrange(2,30)):
               rand_id = random.randrange(2,29)
               commenter = commenters[rand_id]
               wc = ChapterComment(
                       chapter = c,
                       author = commenter,
                       content = "chapter %i 번째 댓글" % x )
               wc.save()
              # create chapter comment
        # create comment
        pass
    def test_work_api(self):
        c = Client()
        #signup_res = c.post("/api/signup/",{
        #        "email":"user1@email.com",
        #        "password":"pass1",
        #        "nickname":"nick1"
        #        })
        #print signup_res
        #users = CubiUser.objects.all()[0]
        #self.assertEqual(users.nickname,"nick1")
