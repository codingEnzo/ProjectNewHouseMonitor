# -*-coding=utf-8-*-
import datetime
import os
import sys

import django
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

from HouseNew.models import *
from services.spider_service import spider_call
from django.conf import settings as dj_settings

import pickle

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=10)
REDIS_CACHE_KEY = "NewHouseTianjin"

default_args = {
    'owner': 'airflow',
    'start_date': STARTDATE,
    'email': ['coder.gsy@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1),
}

spider_settings = {
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesTianjin.PipelineTianjin': 300,
        'HouseCrawler.Pipelines.PipelinesUtils.PipelinesCheck.CheckPipeline': 299,
        'HouseCrawler.Pipelines.PipelinesUtils.PipelinesKafka.KafkaPipeline': 301,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresTianjin.ProjectGetFidMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresTianjin.ProjectDetailMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresTianjin.BuildingDetailMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresTianjin.HouseDetailMiddleware': 105,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 3.5,
    'REDIRECT_ENABLED': True,
    'DEFAULT_REQUEST_HEADERS': {
        "Referer": "http://www.tjfdc.com.cn/Default.aspx",
        "Host": "www.tjfdc.com.cn",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    },
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware': None,
    },
    'RETRY_HTTP_CODES': [500, 403, 404, 501, 502, 503, 504, 400, 408, 411, 413, 407, 303, 304, 305, 306, 307],
    'REDIRECT_ENABLED': True,
    'HTTPERROR_ALLOWED_CODES': [302],
    'DOWNLOAD_DELAY': 0.5,
    'CONCURRENT_REQUESTS': 4,
    'COOKIES_ENABLED': True,
    'CITY': "天津"

}

dag = DAG('NewHouseTianjin', default_args=default_args,
          schedule_interval="15 */8 * * *")

t1 = PythonOperator(
    task_id='LoadProjectListTianjin',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [
                   {'source_url': 'http://www.tjfdc.com.cn/Pages/fcdt/fcdtlist.aspx?SelMnu=FCSJ_XMXX',
                    'meta': {'PageType': 'pl_url'}
                    }
               ]},
    dag=dag
)


def cache_query():
    r = dj_settings.REDIS_CACHE
    cur = ProjectDetailTianjin.objects.aggregate(*[{'$sort': {'RecordTime': -1}},
                                                   {'$group': {'_id': '$ProjectUUID',
                                                               'ProjectName': {'$first': '$ProjectName'},
                                                               'ProjectUUID': {'$first': '$ProjectUUID'},
                                                               'RegionName': {'$first': '$RegionName'},
                                                               }}
                                                   ])
    for item in cur:
        try:
            source_url = "http://www.tjfdc.com.cn/Pages/fcdt/fcdtlist.aspx?SelMnu=FCSJ_XMXX&KPZT=&strKPZT=&QY=&XZQH=&strXZQH=&BK=&XMMC={0}".format(
                item['ProjectName'])
            project_info = {'source_url': source_url,
                            'meta': {
                                'PageType': 'GetProjectFid',
                                'Record_Data': {
                                    "ProjectName": item['ProjectName'],
                                    "RegionName": item['RegionName'],
                                    "ProjectUUID": str(item['ProjectUUID']),
                                }
                            }}
            r.sadd(REDIS_CACHE_KEY, pickle.dumps(project_info))
        except:
            import traceback
            traceback.print_exc()
    r.expire(REDIS_CACHE_KEY, 3600)


t2 = PythonOperator(
    task_id='LoadBuildingDetailTianjinCache',
    python_callable=cache_query,
    dag=dag
)

project_info_generator = map(lambda x: pickle.loads(
    x), dj_settings.REDIS_CACHE.smembers(REDIS_CACHE_KEY))
t3 = PythonOperator(
    task_id='LoadBuildingDetailTianjin',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_generator,
               'spider_count': 10,
               },
    dag=dag)
t3.set_upstream(t2)
