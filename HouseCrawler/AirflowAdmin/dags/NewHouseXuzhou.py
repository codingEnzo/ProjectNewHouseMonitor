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
from django.conf import settings as dj_settings

import pickle

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=10)
REDIS_PROJECT_CACHE_KEY = 'NewHouseProjectXuzhou'
REDIS_PESELL_CACHE_KEY = 'NewHousePresellXuzhou'
REDIS_HOUSE_CACHE_KEY = 'NewHouseHouseXuzhou'

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
        'HouseCrawler.Pipelines.PipelinesXuzhou.PipelineXuzhou': 300,
        'HouseCrawler.Pipelines.PipelinesUtils.PipelinesCheck.CheckPipeline': 299,
        'HouseCrawler.Pipelines.PipelinesUtils.PipelinesKafka.KafkaPipeline': 301,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.ProjectBaseHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.ProjectInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.PresellInfoHandleMiddleware': 106,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.BuildingInfoHandleMiddleware': 107,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.HouseInfoHandleMiddleware': 108,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
    'USER_AGENTS': [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    ],
    'CITY': '徐州'
}

dag = DAG('NewHouseXuzhou', default_args=default_args,
          schedule_interval="20 */8 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseXuzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [{
            'source_url': 'http://www.xzhouse.com.cn/platform/API.do?call&sign=spfService&orderStr=fwl%20desc&PAGE=1&ROWS=9999',
            'meta': {
                'PageType': 'ProjectBase',
                'CurPage': 1
            }
        }]
    }, dag=dag
)


def cache_query():
    r = dj_settings.REDIS_CACHE
    cur = ProjectInfoXuzhou.objects.aggregate(*[
        {'$sort': {'CurTimeStamp': -1}},
        {
            '$group': {
                '_id': '$ProjectUUID',
                'ProjectUUID': {'$first': '$ProjectUUID'},
                'ProjectID': {'$first': '$ProjectID'},
                'ProjectName': {'$first': '$ProjectName'},
            }
        }])
    for item in cur:
        try:
            presell_info = {
                'source_url': 'http://www.xzhouse.com.cn/platform/actionController.do?doQuery&code=item_xsqk&itemid={id}'.format(
                    id=item['ProjectID']),
                'meta': {'PageType': 'PresellInfo',
                         'ProjectID': item['ProjectID'],
                         'ProjectUUID': str(item['ProjectUUID']),
                         'ProjectName': item['ProjectName'],
                         }
            }
            r.sadd(REDIS_PROJECT_CACHE_KEY, pickle.dumps(presell_info))
        except Exception:
            import traceback
            traceback.print_exc()
    r.expire(REDIS_PROJECT_CACHE_KEY, 3600)


t2 = PythonOperator(
    task_id='LoadPresellInfoXuzhouCache',
    python_callable=cache_query,
    dag=dag
)

presell_generator = map(lambda x: pickle.loads(
    x), dj_settings.REDIS_CACHE.smembers(REDIS_PROJECT_CACHE_KEY))
t3 = PythonOperator(
    task_id='LoadPresellXuzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': presell_generator
    },
    dag=dag
)
t3.set_upstream(t2)


def building_cache_query():
    r = dj_settings.REDIS_CACHE
    cur = PresellInfoXuzhou.objects.aggregate(*[
        {'$sort': {'CurTimeStamp': -1}},
        {
            '$group': {
                '_id': '$PresellUUID',
                'PresellUUID': {'$first': '$PresellUUID'},
                'ProjectUUID': {'$first': '$ProjectUUID'},
                'PresellID': {'$first': '$PresellID'},
                'ProjectID': {'$first': '$ProjectID'},
                'ProjectName': {'$first': '$ProjectName'},
                'PresalePermitNumber': {'$first': '$PresalePermitNumber'},
            }
        }])
    for item in cur:
        try:
            presell_info = {
                'source_url': 'http://www.xzhouse.com.cn/platform/actionController.do?doQuery&code=item_lpxx&saleItemid={0}'.format(
                    item['PresellID']),
                'meta': {'PageType': 'BuildingList',
                         'ProjectID': item['ProjectID'],
                         'ProjectUUID': str(item['ProjectUUID']),
                         'PreselltUUID': str(item['PresellUUID']),
                         'ProjectName': item['ProjectName'],
                         'PresalePermitNumber': item['PresalePermitNumber'],
                         }
            }
            r.sadd(REDIS_PESELL_CACHE_KEY, pickle.dumps(presell_info))
        except Exception:
            import traceback
            traceback.print_exc()
    r.expire(REDIS_PESELL_CACHE_KEY, 3600)


t4 = PythonOperator(
    task_id='LoadBuildingCacheXuzhou',
    python_callable=building_cache_query,
    dag=dag
)


building_generator = map(lambda x: pickle.loads(
    x), dj_settings.REDIS_CACHE.smembers(REDIS_PROJECT_CACHE_KEY))
t5 = PythonOperator(
    task_id='LoadBuildingXuzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': building_generator
    },
    dag=dag
)
t5.set_upstream(t4)


def house_cache_query():
    r = dj_settings.REDIS_CACHE
    cur = BuildingInfoXuzhou.objects.aggregate(*[
        {'$sort': {'CurTimeStamp': -1}},
        {
            '$group': {
                '_id': '$BuildingUUID',
                'PresellUUID': {'$first': '$PresellUUID'},
                'ProjectUUID': {'$first': '$ProjectUUID'},
                'BuildingUUID': {'$first': '$BuildingUUID'},
                'ProjectID': {'$first': '$ProjectID'},
                'ProjectName': {'$first': '$ProjectName'},
                'PresalePermitNumber': {'$first': '$PresalePermitNumber'},
                'BuildingID': {'$first': '$BuildingID'},
                'BuildingName': {'$first': '$BuildingName'},
            }
        }])
    for buildingItem in cur:
        try:
            presell_info = {
                'source_url': 'http://www.xzhouse.com.cn/platform/actionController.do?doQuery&code=item_houseinfo&buildingid={0}'.format(
                    buildingItem['BuildingID']),
                'meta': {'PageType': 'HouseList',
                         'ProjectID': buildingItem['ProjectID'],
                         'ProjectUUID': buildingItem['ProjectUUID'],
                         'ProjectName': buildingItem['ProjectName'],
                         'PresellUUID': buildingItem['PresellUUID'],
                         'PresalePermitNumber': buildingItem['PresalePermitNumber'],
                         'BuildingUUID': str(buildingItem['BuildingUUID']),
                         'BuildingName': buildingItem['BuildingName'],
                         }
            }
            r.sadd(REDIS_HOUSE_CACHE_KEY, pickle.dumps(presell_info))
        except Exception:
            import traceback
            traceback.print_exc()
    r.expire(REDIS_HOUSE_CACHE_KEY, 3600)


t6 = PythonOperator(
    task_id='LoadHouseListCacheXuzhou',
    python_callable=house_cache_query,
    dag=dag
)
house_generator = map(lambda x: pickle.loads(
    x), dj_settings.REDIS_CACHE.smembers(REDIS_HOUSE_CACHE_KEY))
t7 = PythonOperator(
    task_id='LoadHouseListXuzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': house_generator
    },
    dag=dag
)
t7.set_upstream(t6)
