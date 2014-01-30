#-*- coding: utf-8 -*-
import urllib
import re
import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
import mechanize
import json

# 리그웹툰(아마추어)
list_url = 'http://cartoon.media.daum.net/league/view/'
rss_url = 'http://webtoon.daum.net/league/rss/'
detail_url = 'http://cartoon.media.daum.net/league/viewer/'
detail_url_json = 'http://cartoon.media.daum.net/data/leaguetoon/viewer_images/'


def list(comic_number):
    ### 작품 정보 ###
    br = mechanize.Browser()
    url_open = '%s%s' % (list_url, comic_number)
    # url_rss = '%s%s' % (rss_url, comic_number)

    response = br.open(url_open)
    soup = BeautifulSoup(response.read())

    # 타이틀 이미지
    div_img_title = soup.find('div', 'wrap_image')
    img_title = div_img_title.find('img')
    comic_url_img_title = img_title['src']

    # 타이틀
    div_title = soup.find('div', 'wrap_title')
    comic_title = div_title.find('span').string

    # 작가명, 장르
    div_cont = soup.find('div', 'wrap_cont')
    dl_list = div_cont.find_all('dl')
    dl_author = dl_list[0]
    dl_genre = dl_list[1]

    comic_author_name = dl_author.dd.string
    comic_genre = dl_genre.dd.contents[0].strip()



    ### 작품 리스트 ###
    url_rss = '%s%s' % (rss_url, comic_number)

    br.open(url_open)
    response = br.open(url_rss)

    data_xml = response.read()
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
            'title': item_title,
            'detail_num': item_detail_num,
            'url_thumbnail': item_url_thumbnail,
            'date': item_date,
        }
        dict_list.append(dict)

    d = {
        'comic_title': comic_title,
        'comic_author_name': comic_author_name,
        'comic_genre': comic_genre,
        'comic_url_img_title': comic_url_img_title,
        'chapter_list': dict_list,
    }

    return d


def detail(detail_num):
    br = mechanize.Browser()
    url_open = '%s%d' % (detail_url, detail_num)
    url_detail = '%s%d' % (detail_url_json, detail_num)

    br.open(url_open)
    response = br.open(url_detail)

    data = json.loads(response.read())
