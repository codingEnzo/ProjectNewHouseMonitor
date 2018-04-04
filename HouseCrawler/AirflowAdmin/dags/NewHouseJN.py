# -*-coding=utf-8-*-
import datetime
import functools
import json
import math
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

REDIS_CACHE_KEY = "NewHouseJN"


def just_one_instance(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        import socket
        try:
            global s
            s = socket.socket()
            host = socket.gethostname()
            s.bind((host, 60223))
        except Exception:
            print('already has an instance')
            return None
        return func(*args, **kwargs)

    return f


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
    # 'end_date': datetime.datetime(2016, 5, 29, 11, 30),
}

spider_settings = {
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesJN.JNPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJN.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJN.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJN.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJN.HouseInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJN.SignInfoHandleMiddleware': 106,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'PROXY_LEVEL': 'high',
    'PROXY_ENABLE': False,
    'RETRY_TIMES': 15
}

dag = DAG('NewHouseJN', default_args=default_args,
          schedule_interval="0 8 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseJN',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://www.jnfdc.gov.cn/onsaling/index.shtml',
                            'meta': {'PageType': 'ProjectBase'}}]},
    dag=dag
)

project_info_list = []
cur = ProjectBaseJinan.objects.all()

for item in cur:
    project_info = {
        'source_url': item.ProjectURL,
        'meta': {'PageType': 'ProjectInfo'}
    }
    project_info_list.append(project_info)

t2 = PythonOperator(
    task_id='LoadProjectInfoJN',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list},
    dag=dag
)


def cacheLoader(key=REDIS_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    cur = BuildingInfoJinan.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
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
index_skip = int(math.ceil(len(building_info_list) / float(3))) + 1
for cur, index in enumerate(list(range(0, len(building_info_list), index_skip))):
    t4 = PythonOperator(
        task_id='LoadBuildingInfoJN_%s' % cur,
        python_callable=spider_call,
        op_kwargs={'spiderName': 'DefaultCrawler',
                   'settings': spider_settings,
                   'urlList': building_info_list[index:index + index_skip],
                   'spider_count': 96},
        dag=dag)
    t4.set_upstream(t3)
