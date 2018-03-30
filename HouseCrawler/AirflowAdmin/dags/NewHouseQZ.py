# -*- coding: utf-8 -*-
import datetime
import os
import sys
import json
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

REDIS_CACHE_KEY = "NewHouseQY"

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=10)

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
    # '
}

spider_settings = {
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQZ.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQZ.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQZ.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQZ.HouseInfoHandleMiddleware': 105,
    },
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesQZ.QZPipeline': 300,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
    'DEFAULT_REQUEST_HEADERS': {'Host': 'www.qzfdc.gov.cn:2015',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Accept-Encoding': 'gzip, deflate',
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Referer': 'http://www.qzfdc.gov.cn:2015/qzjsj_web2/xygs.do?method=fdcxxfb&title=zslp',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': 1}
}

dag = DAG('NewHouseQZ', default_args=default_args,
          schedule_interval="15 8 */2 * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseQZ',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [
            {'source_url': 'http://www.qzfdc.gov.cn:2015/qzjsj_web2/xygs.do?method=fdcxxfb',
             'meta': {'PageType': 'ProjectBase'}}
        ]
    },
    dag=dag
)

project_info_list = []
cur = ProjectBaseQuanzhou.objects.all()
for item in cur:
    project_info = item.ProjectURL
    project_info_list.append(project_info)

t2 = PythonOperator(
    task_id='LoadProjectInfoQZ',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': project_info_list
    },
    dag=dag
)


def cacheLoader(key=REDIS_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    cur = BuildingInfoQuanzhou.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
                                                   {'$group': {
                                                       '_id': "$BuildingUUID",
                                                       'ProjectName': {'$first': '$ProjectName'},
                                                       'ProjectUUID': {'$first': '$ProjectUUID'},
                                                       'BuildingName': {'$first': '$BuildingName'},
                                                       'BuildingUUID': {'$first': '$BuildingUUID'},
                                                       'BuildingURL': {'$first': '$BuildingURL'},
                                                   }}])
    for item in cur:
        try:
            if item['BuildingURL']:
                if True:
                    building_info = {'source_url': item['BuildingURL'],
                                     'meta': {'PageType': 'HouseInfo',
                                              'ProjectName': item['ProjectName'],
                                              'BuildingName': item['BuildingName'],
                                              'ProjectUUID': str(item['ProjectUUID']),
                                              'BuildingUUID': str(item['BuildingUUID'])}}
                    r.sadd(key, json.dumps(building_info))
        except Exception:
            import traceback
            traceback.print_exc()
        r.expire(key, int(spider_settings.get('CLOSESPIDER_TIMEOUT')))


t3 = PythonOperator(
    task_id='LoadBuildingInfoCache',
    python_callable=cacheLoader,
    op_kwargs={'key': REDIS_CACHE_KEY},
    dag=dag)


building_info_list = list(map(lambda x: json.loads(
    x.decode()), dj_settings.REDIS_CACHE.smembers(REDIS_CACHE_KEY)))
t4 = PythonOperator(
    task_id='LoadBuildingInfoQZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': building_info_list},
    dag=dag
)
t4.set_upstream(t3)
