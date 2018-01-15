# -*- coding: utf-8 -*-
import datetime
import os
import sys
import requests
import re
import random

import django
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

BASE_DIR = os.path.abspath(os.environ.get('AIRFLOW_HOME'))
HOUSESERVICECORE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore'))
HOUSEADMIN_DIR = os.path.abspath(os.path.join(BASE_DIR,'ServiceCore/HouseAdmin'))
HOUSECRAWLER_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore/HouseCrawler'))
HOUSESERVICE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore/SpiderService'))

sys.path.append(BASE_DIR)
sys.path.append(HOUSEADMIN_DIR)
sys.path.append(HOUSECRAWLER_DIR)
sys.path.append(HOUSESERVICE_DIR)
sys.path.append(HOUSESERVICECORE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'HouseAdmin.settings'
django.setup()

from HouseNew.models import *
from services.spider_service import spider_call

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=9)

default_args = {
    'owner': 'sun',
    'start_date': STARTDATE,
    'email': ['jiajia.sun@yunfangdata.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime.datetime(2016, 5, 29, 11, 30),
}

spider_settings = {
    'ITEM_PIPELINES': {
         'HouseCrawler.Pipelines.PipelinesWenzhou.Pipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWenzhou.SpiderMiddlerProjectBase': 101,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWenzhou.SpiderMiddlerDeveloperInfo': 102,
    },
    'DOWNLOAD_FAIL_ON_DATALOSS' : False,
    'RETRY_ENABLE': False,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'RETRY_TIMES': 15,
    'CONCURRENT_REQUESTS': 64,
}

dag = DAG(
    'NewHouseWenzhou',
    default_args=default_args,
    schedule_interval="10 */5 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseWenzhou',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://www.wzfg.com/realweb/stat/ProjectSellingList.jsp',
                            'meta': {'PageType': 'ProjectStart'}}]},
    dag=dag
)


DeveloperInfo_list = []

headers = {
    'Host': 'www.wzfg.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
cur = ProjectBaseWenzhou.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                      {'$group':
                                           {'_id': "$ProjectNo",
                                            'Projectname': {'$last': '$Projectname'},
                                            'ProjectNo':{'$last': '$ProjectNo'},
                                            'DeveloperInfoUrl':{'$last': '$DeveloperInfoUrl'}
                                            }
                                       }], allowDiskUse=True)

for item in cur:
    if item['DeveloperInfoUrl']:
        base = {
            'source_url': item['DeveloperInfoUrl'],
            'headers': headers,
            'meta': {
                'PageType': 'DeveloperInfo',
                'ProjectName': item['ProjectName'],
                'ProjectNo': item['ProjectNo']
            }
        }
        DeveloperInfo_list.append(base)
t2 = PythonOperator(
    task_id='LoadDeveloperInfoWenzhou',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': DeveloperInfo_list,
               },
    dag=dag)
