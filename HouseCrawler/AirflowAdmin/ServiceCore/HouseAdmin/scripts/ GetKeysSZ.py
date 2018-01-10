#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import requests
import re
import time

r = redis.Redis(host='10.30.1.18', port=6379)


def get_key():
    mainurl = 'http://spf.szfcweb.com/szfcweb/*/DataSerach/'
    url = 'http://spf.szfcweb.com/szfcweb/DataSerach/SaleInfoProListIndex.aspx'
    mainkey = ''
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Host': 'www.szfcweb.com'}
    try:
        rep = requests.get(url, headers=header)
        mainkey = re.search(r'\(S\((.*?)\)\)', str(rep.url)).group()
        htmltext = str(rep.text).strip().replace(" ", "")
        VIEWSTATE = re.search(
            r'__VIEWSTATE"value="(.*?)"/>', htmltext).group(1)
        VIEWSTATEGENERATOR = re.search(
            r'__VIEWSTATEGENERATOR"value="(.*?)"/>', htmltext).group(1)
        EVENTVALIDATION = re.search(
            r'__EVENTVALIDATION"value="(.*?)"/>', htmltext).group(1)
        req_dict = {
            '__VIEWSTATE': VIEWSTATE,
            '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': EVENTVALIDATION,
            'ctl00$MainContent$txt_Pro': '',
            'ctl00$MainContent$txt_Com': '',
            'ctl00$MainContent$bt_select': '查询',
            'ctl00$MainContent$ddl_RD_CODE': '工业园区'
        }
        repost = requests.post(rep.url, req_dict)

        nexthrf = mainurl.replace("*", mainkey) + re.search(r'SaleInfoBudingShow.aspx\?SPJ_ID=(.*?)"',
                                                            repost.text).group().replace('"', '')
        header['Referer'] = repost.url
        nextrep = requests.get(nexthrf, headers=header)

    except Exception:
        print('get key err')

    return mainkey


def run():
    while True:
        putnum = 10
        for i in range(0, putnum):
            key = get_key()
            r.set('SuzhouCrawlerkey%d' % i, key)
            r.expire('SuzhouCrawlerkey%d' % i, 50)
            print('get key')
            time.sleep(5)
