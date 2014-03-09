#-*- coding: utf-8 -*-
import urllib, urllib2
import re
import StringIO
from bs4 import BeautifulSoup
from datetime import datetime, date

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
        url = 'http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%s&weekday=tue' % ( id, no )
        page = BeautifulSoup(urllib.urlopen(url))
        images = page.select('div.wt_viewer img')
        thumb = StringIO.StringIO()
        thumb.write(urllib.urlopen(page.select('#comic_move a.on img')[0]['src']).read())
        thumb.close()
        data = {
            'title': page.select('div.tit_area h3')[0].text,
            'thumbnail': thumb,
            'date': datetime.strptime(page.select('dl.rt dt + dd.date')[0].text, '%Y.%m.%d').date(),
            'images': []
        }

        for image in images:
            if image['src'] == '':
                break
            request = urllib2.Request(image['src'])
            request.add_header('Referer', url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
            tmp = StringIO.StringIO()
            tmp.write(urllib2.urlopen(request).read())
            tmp.close()
            data['images'].append(tmp)

        return data

# exmaple
# print NaverWebtoon().list(81482)
# print NaverWebtoon().detail(81482, 446)