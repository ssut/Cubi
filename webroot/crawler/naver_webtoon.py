#-*- coding: utf-8 -*-
import urllib
import re
import StringIO
from bs4 import BeautifulSoup
from datetime import datetime, date
# pip install beautifulsoup4

class NaverWebtoon(object):
    _instance = None
    _thead = re.compile(r'\<thead>(.*?)\<\/thead>', re.MULTILINE)
    _no = re.compile(r'&no=([0-9]+)')
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NaverWebtoon, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def list(self, id):
        # 마지막 페이지 번호
        last = BeautifulSoup(urllib.urlopen('http://comic.naver.com/webtoon/list.nhn?titleId=%s&weekday=tue&page=99999' % ( id )))
        last = int(last.select('span.current')[0].text)

        items = []
        for i in range(1, last + 1):
            page = BeautifulSoup(urllib.urlopen('http://comic.naver.com/webtoon/list.nhn?titleId=%s&weekday=tue&page=%s' % ( id, i )))
            table = str(page.select('table.viewList')[0]).replace('\n', '')
            table = BeautifulSoup(self._thead.sub('', table))
            tr = table.select('tr')
            tr.pop(0)

            for row in tr:
                no = int(self._no.search(row.select('a')[0]['href']).group(1))
                thumbnail = row.select('img')[0]['src']
                title = row.select('img')[0]['title']
                rating = row.select('span.star + strong')[0].text
                date = datetime.strptime(row.select('td.num')[0].text, '%Y.%m.%d').date()

                items.append({
                    'no': no,
                    'thumbnail': thumbnail,
                    'title': title,
                    'rating': rating,
                    'date': date,
                })

        return items

    def detail(self, id, no):
        page = BeautifulSoup(urllib.urlopen('http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%s&weekday=tue' % ( id, no )))
        images = page.select('div.wt_viewer img')
        data = []

        for image in images:
            url = image['src']
            tmp = StringIO.StringIO()
            tmp.write(urllib.urlopen(url).readlines())
            tmp.close()
            data.append(tmp)

       return data
    
# exmaple
# NaverWebtoon().list(81482)
# NaverWebtoon().detail(81482, 446)