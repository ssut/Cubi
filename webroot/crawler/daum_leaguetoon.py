# -*- coding: utf-8 -*-
import StringIO
import json
import re
import urllib

import mechanize

from bs4 import BeautifulSoup
from datetime import datetime

from .exceptions import WebtoonDoesNotExist, WebtoonChapterDoesNotExist

# 리그웹툰(아마추어)
list_url = 'http://cartoon.media.daum.net/league/view/'
rss_url = 'http://webtoon.daum.net/league/rss/'
detail_url = 'http://cartoon.media.daum.net/league/viewer/'
detail_json = 'http://cartoon.media.daum.net/data/leaguetoon/viewer_images/'

def info(comic_number):
    # 작품 정보
    br = mechanize.Browser()
    url_open = '%s%s' % (list_url, comic_number)

    try:
        response = br.open(url_open)
        soup = BeautifulSoup(response.read())
    except Exception, e:
        raise WebtoonDoesNotExist()

    # 타이틀 이미지
    div_img_title = soup.find('div', 'wrap_image')
    img_title = div_img_title.find('img')
    comic_url_img_title = img_title['src']

    # 타이틀
    div_title = soup.find('div', 'wrap_title')
    comic_title = div_title.find('h3')['title']

    # 작가명, 장르
    div_cont = soup.find('div', 'wrap_cont')
    dl_list = div_cont.find_all('dl')
    dl_author = dl_list[0]
    dl_genre = dl_list[1]

    comic_author_name = dl_author.dd.string
    comic_genre = dl_genre.dd.contents[0].strip()

    # 작품소개
    div_more = soup.find('div', 'wrap_more')
    dl_description = div_more.find_all('dl')[0]
    comic_description = dl_description.dd['title']

    info = {
        'title': comic_title,
        'author': comic_author_name,
        'description': comic_description,
        'genre': comic_genre,
        'title_image': comic_url_img_title,
    }

    return info

def list(comic_number):
    # 작품 정보
    br = mechanize.Browser()

    # 작품 리스트
    url_rss = '%s%s' % (rss_url, comic_number)

    try:
        response = br.open(url_rss)
        data_xml = response.read()
    except Exception, e:
        raise WebtoonDoesNotExist()

    soup = BeautifulSoup(data_xml, 'xml')

    dict_list = []
    items = soup.find_all('item')
    for item in items:
        # 제목
        item_title = item.title.string

        # detail_num
        link = item.link.string
        con_link = re.compile(r'.*viewer\/(.*)')
        item_detail_num = con_link.search(link).group(1)

        # 썸네일 이미지 URL
        description = item.description.string
        con_img = re.compile(r'src=\'(.*?)\'')
        item_url_thumbnail = con_img.search(description).group(1)

        # 날짜
        pubdate = item.pubDate.string
        item_date = datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')

        dict = {
            'no': item_detail_num,
            'thumbnail': item_url_thumbnail,
            'title': item_title,
            'rating': '',
            'date': item_date,
        }
        print '%s] %s (%s)' % (dict['no'], dict['title'], dict['date'])
        dict_list.append(dict)
    dict_list.reverse()

    return dict_list


def detail(detail_num):
    br = mechanize.Browser()
    url_open = '%s%s' % (detail_url, detail_num)
    url_detail = '%s%s' % (detail_json, detail_num)

    try:
        page = BeautifulSoup(br.open(url_open).read())

        br.open(url_open)
        response = br.open(url_detail)
    except Exception, e:
        pass

    title = page.select('span.episode_title')[0].text

    selector = 'div.episode_list ul li a[href$="%s"] img' % (detail_num)
    thumb = StringIO.StringIO()
    thumb.write(urllib.urlopen(page.select(selector)[0]['src']).read())
    thumb.seek(0)

    data = {
        'no': detail_num,
        'title': title,
        'thumbnail': thumb,
        'date': datetime.now(),  # 다음 detail 페이지에서는 날짜 정보를 보내주지 않음
        'images': []
    }

    # Sequence 이미지 리스트
    image_list = []
    info_list = json.loads(response.read())['data']
    for info in info_list:
        image_name = info['name']
        image_url = info['url']
        image_order = info['imageOrder']

        tmp = StringIO.StringIO()
        tmp.write(urllib.urlopen(image_url).read())
        tmp.seek(0)
        data['images'].append(tmp)

    return data
