# -*- coding: utf-8 -*-
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

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=8)

default_args = {
    'owner': 'airflow',
    'start_date': STARTDATE,
    'email': ['coder.gsy@gmail.com'],
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
        'HouseCrawler.Pipelines.PipelinesNJ.NJPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresNJ.SpiderMiddlerGetBase': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresNJ.SpiderMiddlerDeveloper': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresNJ.SpiderMiddlerPresale': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresNJ.SpiderMiddlerProject': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresNJ.SpiderMiddlerBuilding': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresNJ.SpiderMiddlerHouse': 107,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.6,
    'CONCURRENT_REQUESTS': 64,
}

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Connection': "keep-alive",
    'Host': "www.njhouse.com.cn",
    'Cache-Control': "max-age=0",
}

urlClass = {
    "PresaleBase": "http://www.njhouse.com.cn/2016/spf/persalereg.php",
    "ProjectBase": "http://www.njhouse.com.cn/2016/spf/list.php?dist=&use=&saledate=&per_name=",
    "DeveloperBase": "http://www.njhouse.com.cn/2016/qy/index.php?lanmu=&keyword=&pgno=1"
}

dag = DAG('NewHouseNJ', default_args=default_args,
          schedule_interval="15 6 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseNJ',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [
            {'source_url': url,
             'headers': headers,
             'meta': {'PageType': 'GetPageBase'}} for url in urlClass.values()
        ]
    },
    dag=dag
)
