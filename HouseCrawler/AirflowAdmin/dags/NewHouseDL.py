# -*-coding=utf-8-*-
import os
import sys
import django
import json
import datetime
import functools
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

REDIS_CACHE_KEY = "NewHouseDL"


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


STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=14)

default_args = {
    'owner': 'airflow',
    'start_date': STARTDATE,
    'email': ['1012137875@qq.com'],
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
        'HouseCrawler.Pipelines.PipelinesDL.DLPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresDL.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresDL.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresDL.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresDL.HouseInfoHandleMiddleware': 105,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 3.5
}


dag = DAG('NewHouseDL', default_args=default_args,
          schedule_interval="45 */12 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseDL',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://old.gtfwj.dl.gov.cn/bd/tgxm',
                            'meta': {'PageType': 'ProjectBase'}}]},
    dag=dag)

project_info_list = []
cur = ProjectBaseDalian.objects.filter(CurTimeStamp__gte="2018-04-01 00:00:00")
for item in cur:
    project_info = {'source_url': item.ProjectURL,
                    'meta': {'PageType': 'ProjectInfo'}}
    project_info_list.append(project_info)
t2 = PythonOperator(
    task_id='LoadProjectInfoDL',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list},
    dag=dag)


def cacheLoader(key=REDIS_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    cur = BuildingInfoDalian.objects.aggregate(*[{'$match': {'CurTimeStamp': {'$gte': "2018-04-01 00:00:00"}}},
                                                 {"$sort": {"CurTimeStamp": -1}},
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
    task_id='LoadBuildingInfoDL',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': building_info_list},
    dag=dag)
t4.set_upstream(t3)
