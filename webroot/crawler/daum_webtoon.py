# -*- coding: utf-8 -*-
import urllib
import re
import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
import mechanize
import json

# 정식웹툰
list_url = 'http://cartoon.media.daum.net/webtoon/view/'
comic_title = 'dogandrabbit'

detail_url = 'http://cartoon.media.daum.net/webtoon/viewer/'
detail_url_json = "http://cartoon.media.daum.net/webtoon/" \
                  "viewer_images.js?webtoon_episode_id="

# 정식웹툰
def detail(detail_num):
    # mechanize를 이용해서 detail_url에서 쿠키얻어 저장한 뒤(자동)
    # detail_url_json에 요청해야만 값 받아옴
    br = mechanize.Browser()
    url_open = '%s%d' % (detail_url, detail_num)
    url_detail = '%s%d' % (detail_url_json, detail_num)

    br.open(url_open)
    response = br.open(url_detail)

    # json형식으로 데이터 받아옴. episodeTitle과 images를 사용
    data = json.loads(response.read())
    episode_title = data['episodeTitle']

    imgs = data['images']
    img_src_list = []
    for img in imgs:
        img_src = img['url']
        img_src_list.append(img_src)

    # 현재 화의 제목과 이미지 경로 목록을 리턴
    d = {
        'episode_title': episode_title,
        'img_src_list': img_src_list,
    }
    return d

# 웹툰의 리스트정보 반환
def list(comic_title):
    data = urllib.urlopen(list2_url + comic_title)
    soup = BeautifulSoup(data)

    div_wrap_title = soup.find('div', 'wrap_title')
    comic_title = div_wrap_title.find('img')['alt']

    # 작가이름
    author_name = soup.find('dd', 'desc_author').string

    # 작품정보
    div_comic_info = soup.find('div', 'wrap_more')
    dl_list_intro = div_comic_info.find('dl', 'list_intro')
    comic_description = dl_list_intro.contents[3].string

    # 아이콘
    div_icon = soup.find('div', 'wrap_image')
    icon_src = div_icon.find('img')['src']

    # 장르, 등급
    dl_list_more_info = div_comic_info.find('dl', 'list_more_info')
    comic_genre = dl_list_more_info.contents[3].string
    comic_grade = dl_list_more_info.contents[7].string

    # 회차정보 얻어오기
    scripts = soup.find_all('script')

    # data1(회차정보 담긴 자바스크립트 변수) 이 들어있는 string_data1 얻기
    for i in range(len(scripts)):
        script = scripts[i]
        if script.string:
            if 'data1' in script.string:
                string_data1 = script.string
            else:
                pass
        else:
            pass

    con = re.compile(r'data1.*?\{(.*?)\}')
    data1_list = con.findall(string_data1)

    con_img = re.compile(r'img : \"(.*?)\"')
    con_title = re.compile(r'title:\"(.*?)\"')
    con_short_title = re.compile(r'shortTitle:\"(.*?)\"')
    con_url = re.compile(r'url:\"(.*?)\"')
    con_date = re.compile(r'date:\"(.*?)\"')

    con_chapter_number = re.compile(r'viewer/(.*)')

    # 회차정보 리스트
    chapter_list = []
    for data1 in data1_list:
        url_thumbnail = con_img.search(data1).group(1)
        title = con_title.search(data1).group(1)
        short_title = con_short_title.search(data1).group(1)
        chapter_url = con_url.search(data1).group(1)
        chapter_number = con_chapter_number.search(chapter_url).group(1)

        strdate = con_date.search(data1).group(1)
        chapter_date = datetime.strptime(strdate, '%Y.%m.%d').date()

        chapter_info = {
            'url_thumbnail': url_thumbnail,
            'title': title,
            'short_title': short_title,
            'chapter_url': chapter_url,
            'chapter_number': chapter_number,
            'strdate': strdate,
            'date': chapter_date,
        }
        # print chapter_info
        chapter_list.append(chapter_info)

    # 제목, 작가명, 작품정보, 이용가, 장르, 각 화 chapter_number 를 포함한
    # chapter_info 리스트 반환
    d = {
        'comic_title': comic_title,
        'author_name': author_name,
        'comic_icon': icon_src,
        'comic_description': comic_description,
        'comic_grade': comic_grade,
        'comic_genre': comic_genre,
        'chapter_list': chapter_list,
    }

    return d
