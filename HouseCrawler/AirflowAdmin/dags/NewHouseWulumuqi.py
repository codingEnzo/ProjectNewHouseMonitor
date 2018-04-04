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


default_args = {
    'owner': 'airflow',
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
        'HouseCrawler.Pipelines.PipelinesWulumuqi.PipelineWulumuqi': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWulumuqi.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWulumuqi.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWulumuqi.PresellInfoHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWulumuqi.PresellListHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWulumuqi.HouseListHandleMiddleware': 106,

    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    },
    'POST_DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware': None,
    }
}

dag = DAG('NewHouseWulumuqi', default_args=default_args,
          schedule_interval="30 8 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseWulumuqi',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [
            {'source_url': 'http://www.anju-365.com/newhouse/property_searchall.htm?districtid=&sid=&searchkeyword=&keyword=',
             'meta': {'PageType': 'ProjectBase', 'curPage': 1}}
        ]
    },
    dag=dag
)
