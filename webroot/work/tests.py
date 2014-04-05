#-*- coding: utf-8 -*-
from django.test import TestCase
from django.conf import settings

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from datetime import datetime
from django.utils.timezone import now
from django.test.client import Client

from member.models import *
from work.models import *
from work import crawl as crawler

import random
import json

import sys, os
import filecmp
import shutil
import datetime
import glob

import hashlib

def md5_file(filePath, cmp_result=False):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        if cmp_result is True:
            return TColor.OKGREEN + m.hexdigest() + TColor.ENDC
        else:
            return TColor.FAIL + m.hexdigest() + TColor.ENDC

class TColor:
    BOLD = "\033[1m"
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class CrawlTests(TestCase):
    def setUp(self):
        # 임시 유저 생성
        self.user = User.objects.create(type='1', username='test', nickname='test',
            gender='M', tel='000', access_token='000', last_name='a', first_name='b')
        self.user.save()

        # 폴더 구조
        today = now().today()
        today_str = today.strftime('%Y%m%d')
        self.path = os.path.join(settings.MEDIA_PATH, today_str, 'work', 'webtoon')

        # media 폴더가 존재하면 옮겨두고 새로 만들기
        tmp_path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, '..', '_media'))
        if os.path.exists(settings.MEDIA_ROOT) and not os.path.exists(tmp_path):
            os.renames(settings.MEDIA_ROOT, tmp_path)
            os.makedirs(settings.MEDIA_ROOT)

    def test_naver_webtoon_match(self):
        # 네이버 웹툰 크롤링
        result = crawler.crawl(type=ChapterQueue.NAVER, comic_number=81482,
            chapter_number=1, user=self.user)
        self.assertEqual(result, True)

        print '\n  << NAVER WEBTOON CRAWLING TEST >>'
        cmp_result = self.__compare_file__(1)
        self.assertEqual(cmp_result, True)

    def test_daum_webtoon_match(self):
        # 다음 웹툰 크롤링
        result = crawler.crawl(type=ChapterQueue.DAUM, comic_number=8504,
            chapter_number=50136, user=self.user)
        self.assertEqual(result, True)

        print '\n  << DAUM WEBTOON CRAWLING TEST >>'
        cmp_result = self.__compare_file__(2)
        self.assertEqual(cmp_result, True)

    # 파일 비교
    def __compare_file__(self, id):
        originals = glob.glob(os.path.abspath(os.path.join('.', 'work', 'test_assets', str(id) + '_*')))
        downloads = glob.glob(os.path.abspath(os.path.join(self.path, '1_*')))
        for i, orig in enumerate(originals):
            basename = os.path.basename(orig)
            cmp_result = filecmp.cmp(orig, downloads[i])
            print TColor.HEADER + TColor.BOLD + '  {0}\n    {1}{2}\n    {3}{4}    ..{5}'.format(
                basename.ljust(20) + TColor.ENDC,
                'Original File'.ljust(20), md5_file(orig, cmp_result),
                'Downloaded File'.ljust(20), md5_file(downloads[i], cmp_result),
                ('OK' if cmp_result is True else 'FAIL'))
            if cmp_result is False:
                return False
        return True

    # 테스트가 끝나고 media 폴더를 옮겨뒀다면 원상복귀
    def __del__(self):
        tmp_path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, '..', '_media'))
        if os.path.exists(tmp_path):
            shutil.rmtree(settings.MEDIA_ROOT)
            os.renames(tmp_path, settings.MEDIA_ROOT)

class WorkTest(TestCase):
    def setUp(self):
        return
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
        return
        c = Client()
        work_list = c.post("/api/work/list/")
        print "work mobile api list result", work_list
        work_data = json.loads(work_list.content)
        for work in work_data["works"]:
            # get work comment
            comment_list = c.post("/api/work/comment/list/",{"work_id": work["id"]})
            print "work mobile api comment list result", comment_list
            
        #print signup_res
        #users = CubiUser.objects.all()[0]
        #self.assertEqual(users.nickname,"nick1")
