# -*- coding: utf-8 -*-
import datetime
import json
import os
import sys
import uuid
import django
import urllib.parse as urlparse

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

BASE_DIR = os.path.abspath(os.environ.get('AIRFLOW_HOME'))
HOUSESERVICECORE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore'))
HOUSEADMIN_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'ServiceCore/HouseAdmin'))
HOUSECRAWLER_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'ServiceCore/HouseCrawler'))
HOUSESERVICE_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'ServiceCore/SpiderService'))

sys.path.append(BASE_DIR)
sys.path.append(HOUSEADMIN_DIR)
sys.path.append(HOUSECRAWLER_DIR)
sys.path.append(HOUSESERVICE_DIR)
sys.path.append(HOUSESERVICECORE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'HouseAdmin.settings'
django.setup()

from django.conf import settings as dj_settings
from HouseNew.models import *
from services.spider_service import spider_call


STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=6)
REDIS_CACHE_KEY = "NewHouseZS"

default_args = {
    'owner': 'airflow',
    'start_date': STARTDATE,
    'email': ['coder.gsy@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'depends_on_past': False,
    'retries': 1,
    'provide_context': True,
    'retry_delay': datetime.timedelta(minutes=1),
}

spider_settings = {
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesZS.ZSPipeline': 300,
    },
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':
        110,
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.RandomUserAgent':
        1,
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware':
        100,
        'HouseCrawler.DownloadMiddleWares.RetryMiddleWares.RetryMiddleware':
        120,
        # 'HouseCrawler.DownloadMiddleWares.DownloaderMiddleWareZS.HouseInfoDownloaderMiddlerware':
        # 119
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZS.ProjectBaseHandleMiddleware':
        102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZS.ProjectInfoHandleMiddleware':
        103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZS.PresaleLicenceHandleMiddleware':
        104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZS.HouseInfoHandleMiddleware':
        105,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 3.5,
}

dag = DAG(
    'NewHouseZS', default_args=default_args, schedule_interval="15 */4 * * *")


def get_project_base_list(**kwargs):
    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image"
        "/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":
        "gzip, deflate",
        "Accept-Language":
        "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control":
        "no-cache",
        "Connection":
        "keep-alive",
        "Content-Type":
        "application/x-www-form-urlencoded",
        "Host":
        "www.zsfdc.gov.cn:9043",
        "Origin":
        "http://www.zsfdc.gov.cn:9043",
        "Pragma":
        "no-cache",
        "Referer":
        "http://www.zsfdc.gov.cn:9043/pub_ProjectQuery.aspx",
        "Upgrade-Insecure-Requests":
        "1",
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OSX 10_13_1)"
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
        "63.0.3239.84 Safari/537.36"
    }
    zs_areas = [
        ("01", "火炬开发区"),
        ("02", "石岐区"),
        ("03", "东区"),
        ("04", "西区"),
        ("05", "南区"),
        ("06", "小榄镇"),
        ("07", "黄圃镇"),
        ("08", "阜沙镇"),
        ("09", "三角镇"),
        ("10", "东凤镇"),
        ("11", "南头镇"),
        ("12", "古镇镇"),
        ("13", "东升镇"),
        ("14", "港口镇"),
        ("15", "民众镇"),
        ("16", "横栏镇"),
        ("17", "沙溪镇"),
        ("18", "大涌镇"),
        ("19", "南朗镇"),
        ("20", "板芙镇"),
        ("21", "五桂山"),
        ("22", "三乡镇"),
        ("23", "神湾镇"),
        ("24", "坦洲镇"),
    ]
    post_data = {
        "__EVENTTARGET":
        "",
        "__EVENTARGUMENT":
        "",
        "__VIEWSTATE":
        "l8/n7t5xZXl71XhNsvXC//rkgvZGegJbm/N43RyLKSydPjrV9nPgAw9H3j963UpASG75tmTE8LKNyEJUi8mE3FLNsJ0K0+rFBRTznAzomtx3/5Ih9ZvpVC9p4g6IXCirRqUpRstU+vOz5wQjd6GOkBHvSbTIfMGB9Wi96RHTIriqjkuf9k11BZR89VAQEqgAuHKugzlN+Dm4coYpcnhXWoWZLQajNh3AL4X54kNIQd41f0dzku0Tk9IXR49lpT2qtFILrKiGpaX9BLdRbSIiE0Zt+TYieL/Pp//vzJYvOHr9pJgDVdFoCNFDx6zffWaQix3H5zVz1/TT4NQd7hVVSTrNmCRLgyH8bCty5DuJL8dXCBTz7eStsA7R3ZfV8TQjY0XfH7Od20+c2bk16zkgrOKFVDBf7gW8g7XV5ER5DSi+UQMa4+6tBnyFvjwezxSVaR0d8JuInicWSELfVyqbcsuUmfiUTChH/FC3b7s2PuYqwVubOQLeuz+6055YduIiQOaIbJHjns0H2ZlyAqfsgZbMFDbKHY63Fae6OPHNi3xAMDfGNVe32TrSEyP6XDd6oIxcP/qXwbBGlZDRnopnJrwvvO5EJPd6pazE2mW5erXBW1JxgFpoiKjz5UIHyNUoP78ufxvd+ueqiXs/IVw8GqU2RkcKt1fuTf0cknYMve5kJjgHF4Rn79I/dVH1D4ELfNOQSXGCkzEaiTBK341W1GS6a4JPNB2UZnOmdLmYyO1kGNdEIdAlw10wgCou1Y9xHWn1y4mVwpGARvL4+xGqn+D+4MNK4ZFJjFmgyMm3PNXRH36FDxlukU0WHCt5gawupsxU8fTk1eUARGJFtt2UZ0vp5zUiNJQx7htKYwD89Lzut1KswJ3w5ONhxH0bmcqywQekR5KSzLo0qWcxnIYBE2zvx33O1LyBfiRFZSdsCQeBRqYe2d7MROGSH85m1EE2rCFOSgwCFey+KRa4rqZMjJbq2j41QkdN99nkAEuRTGslhMw5VXsYVHBJCnXZeeV+jt8k0pmIvFpqY0J5l3E1pJM3kkjpIKU+0HIckTlzjiJQynhMZaAjtsxaU9g5S8AbYSBjtNc7EVgd3wEEQVvtOSRkw4MACkKlitAouA==",
        "__EVENTVALIDATION":
        "SYf959dYiECdQD8FElc7P7iJmgeoGeI9EqPkA8bAieDy6c7zYQIbAqPFfaf16//1ReElmNoI/YBbwNWrOXEdX15+C7OO9y0zf3KEZTpIlNylgR8DKgZHerxi5pZlk2RZC9nPzscOulXP1lSKO0N7iFqmBg0jEj/fYMrikVi6M5Svf4/0iLHgIEIKJ0qacr4D06CVRzArxCBtZs4rF1cPwWyn4hZ4sYEeLF3I0TCQBtHWt5bEGMel9Px68kJdBeXo08L2eDHBM4ML7RsSXrWWv4KfhHf6H8Vn5H2XVsrU+6XNj5hGvEkxcZ49dGw7I2E2U9vk92qrJuBZiGIjJ9qd0RBD6Zb8SgqnTGkuuX6WZwdAM4EqHkeJif2kEFbsawALRl1cts+tWf97Uidi",
        "searchinput":
        "",
        "ctl00$ContentPlaceHolder1$tbxProjectName":
        "",
        "ctl00$ContentPlaceHolder1$ddlDistrict":
        "01",
        "ctl00$ContentPlaceHolder1$tbxAddress":
        "",
        "ctl00$ContentPlaceHolder1$tbxDeveloper":
        "",
        "ctl00$ContentPlaceHolder1$tbxPrescaleCert":
        "",
        "ctl00$ContentPlaceHolder1$ImageButton1.x":
        "20",
        "ctl00$ContentPlaceHolder1$ImageButton1.y":
        "15",
        "ctl00$ContentPlaceHolder1$newPage":
        "",
    }
    r = dj_settings.REDIS_CACHE
    key = uuid.uuid1().hex
    for i, _area in enumerate(zs_areas):
        _area_id, _area_name = _area
        post_data["ctl00$ContentPlaceHolder1$ddlDistrict"] = _area_id
        body = urlparse.urlencode(post_data)
        project_base = {
            'source_url': "http://www.zsfdc.gov.cn:9043/pub_ProjectQuery.aspx",
            'method': 'GET',
            'body': body,
            'headers': headers,
            'meta': {
                'PageType': 'ProjectInitial',
                'ProjectAdminArea': _area_name,
                'ProjectAdminAreaNum': _area_id
            }
        }
        r.sadd(key, json.dumps(project_base))
    r.expire(key, int(spider_settings.get('CLOSESPIDER_TIMEOUT')))
    return key


def crawl(spiderName='DefaultCrawler',
          settings=None,
          fromTask=None,
          urlList=None,
          **kwargs):
    if fromTask or urlList:
        if not urlList:
            urlList = list(
                map(lambda x: json.loads(x.decode()),
                    dj_settings.REDIS_CACHE.smembers(
                        kwargs['ti'].xcom_pull(task_ids=fromTask))))
        spider_call(
            spiderName='DefaultCrawler', settings=settings, urlList=urlList)


t1_cache = PythonOperator(
    task_id='LoadProjectBaseZSCache',
    python_callable=get_project_base_list,
    dag=dag)

t1 = PythonOperator(
    task_id='LoadProjectBaseZS',
    python_callable=crawl,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'fromTask': 'LoadProjectBaseZSCache'
    },
    dag=dag)

t1.set_upstream(t1_cache)


def get_project_info_list(**kwargs):
    key = uuid.uuid1().hex
    r = dj_settings.REDIS_CACHE
    cur = ProjectBaseZhongshan.objects
    for item in cur:
        project_info = {
            'source_url': item.ProjectInfoURL,
            'meta': {
                'PageType': 'ProjectInfo',
                'ProjectUUID': item.ProjectUUID.hex,
                'ProjectName': item.ProjectName,
                'PresaleNum': item.PresaleNum,
                'ProjectPermitDate': item.ProjectPermitDate
            }
        }
        project_info_json = json.dumps(project_info, sort_keys=True)
        r.sadd(key, project_info_json)
    r.expire(key, int(spider_settings.get('CLOSESPIDER_TIMEOUT')))
    return key


t2_cache = PythonOperator(
    task_id='LoadProjectInfoZSCache',
    python_callable=get_project_info_list,
    dag=dag)

t2 = PythonOperator(
    task_id='LoadProjectInfoZS',
    python_callable=crawl,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'fromTask': 'LoadProjectInfoZSCache'
    },
    dag=dag)

t2.set_upstream(t2_cache)


def get_cookies_list(**kwargs):
    key = uuid.uuid1().hex
    r = dj_settings.REDIS_CACHE
    headers = {
        'Host':
        'www.zsfdc.gov.cn:9043',
        'Connection':
        'keep-alive',
        'Pragma':
        'no-cache',
        'Cache-Control':
        'no-cache',
        'Accept':
        'text/html, */*',
        'Origin':
        'http://www.zsfdc.gov.cn:9043',
        'X-Requested-With':
        'XMLHttpRequest',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Content-Type':
        'application/x-www-form-urlencoded',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9'
    }
    headers_housemain = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9',
        'Cache-Control':
        'no-cache',
        'Connection':
        'keep-alive',
        'Host':
        'www.zsfdc.gov.cn:9043',
        'Pragma':
        'no-cache',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    cur = BuildingInfoZhongshan.objects.aggregate(*[{
        "$sort": {
            "CurTimeStamp": 1
        }
    }, {
        '$group': {
            '_id': "$BuildingUUID",
            'ProjectName': {
                '$first': '$ProjectName'
            },
            'ProjectUUID': {
                '$first': '$ProjectUUID'
            },
            'BuildingName': {
                '$first': '$BuildingName'
            },
            'BuildingUUID': {
                '$first': '$BuildingUUID'
            },
            'HouseInfoURLArgs': {
                '$first': '$HouseInfoURLArgs'
            },
        }
    }])
    for item in cur:
        try:
            if item['HouseInfoURLArgs']:
                args = item['HouseInfoURLArgs'].split(';')
                if len(args) == 5:
                    rec, bnum, sbk, addr, sid = args
                    referer = 'http://www.zsfdc.gov.cn:9043/Housemain.aspx?recnumgather={}&buildnum={}'.format(
                        rec, bnum)
                    cookies = {'ASP.NET_SessionId': sid, 'sbk': sbk}
                    headers['Referer'] = referer
                    url = 'http://www.zsfdc.gov.cn:9043/build.axd'
                    post_data = {
                        'task': 'buildtable',
                        'recnumgather': rec,
                        'buildnum': bnum,
                        'sbk': sbk,
                        'generate': 'false'
                    }
                    body = urlparse.urlencode(post_data)
                    building_info = {
                        'source_url': url,
                        'meta': {
                            'PageType': 'HouseInfo',
                            'ProjectName': item['ProjectName'],
                            'BuildingName': item['BuildingName'],
                            'ProjectUUID': str(item['ProjectUUID']),
                            'BuildingUUID': str(item['BuildingUUID']),
                            'cookies': cookies,
                            'referer': referer
                        },
                        'method': 'POST',
                        'headers': headers,
                        'body': body,
                        'cookies': cookies,
                        'referer': referer
                    }
                    building_info_json = json.dumps(
                        building_info, sort_keys=True)
                    r.sadd(key, building_info_json)
        except Exception as e:
            import traceback
            traceback.print_exc()
    r.expire(key, int(spider_settings.get('CLOSESPIDER_TIMEOUT')))
    return key


t3_cache = PythonOperator(
    task_id='LoadBuildingInfoZSCache',
    python_callable=get_cookies_list,
    dag=dag)

t3 = PythonOperator(
    task_id='LoadBuildingInfoZS',
    python_callable=crawl,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'fromTask': 'LoadBuildingInfoZSCache'
    },
    dag=dag)

t3.set_upstream(t3_cache)
