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

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=6)
REDIS_CACHE_KEY = "NewHouseXA"

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
        'HouseCrawler.Pipelines.PipelinesXA.XAPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.ProjectInfoHandleMiddleware': 103,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.PresaleLicenceHandleMiddleware': 104,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.HouseInfoHandleMiddleware': 105,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 3.5,
    'REDIRECT_ENABLED': False,
    'DOWNLOADER_MIDDLEWARES': {
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.RandomUserAgent': 1,
        'HouseCrawler.DownloadMiddleWares.RetryMiddleWares.RetryMiddleware': 120,
    },
    'DOWNLOAD_DELAY': 1.75,
    'RANDOMIZE_DOWNLOAD_DELAY': True
}

dag = DAG('NewHouseXA', default_args=default_args,
          schedule_interval="15 */4 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseXA',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://www.fang99.com/buycenter/buildingsearch.aspx?page=1',
                            'meta': {'PageType': 'ProjectInitial'}}]},
    dag=dag
)


def query_mongodb(obj=None, name="ProjectBase", key=REDIS_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    try:
        if obj and name == "ProjectBase":
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': 'b.fang99.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            }

            cur = obj.objects.all()
            for item in cur:
                project_info = {
                    'source_url': item.ProjectBaseSubURL,
                    'meta': {
                        'PageType': 'ProjectSubBase',
                        'ProjectUUID': item.ProjectUUID,
                        'ProjectName': item.ProjectName,
                        'ProjectCompany': item.ProjectCompany,
                    },
                    'headers': headers
                }
                r.sadd(key, pickle.dumps(project_info))

            r.expire(key, 86400)
    except Exception:
        import traceback
        traceback.print_exc()


t2 = PythonOperator(
    task_id='LoadProjectInfoCache',
    python_callable=query_mongodb,
    op_kwargs={'key': REDIS_CACHE_KEY, 'obj': ProjectBaseXian, 'name': 'ProjectBase'},
    dag=dag
)

project_info_generator = map(lambda x: pickle.loads(x), dj_settings.REDIS_CACHE.smembers(REDIS_CACHE_KEY))

t3 = PythonOperator(
    task_id='LoadProjectInfo',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_generator},
    dag=dag)
