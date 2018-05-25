# -*-coding=utf-8-*-
import os
import sys
import django
import json
import datetime
import uuid
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

REDIS_CACHE_KEY = "NewHouseCQ"

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
    'provide_context': True
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime.datetime(2016, 5, 29, 11, 30),
}

spider_settings = {
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesCQ.CQPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCQ.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCQ.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCQ.HouseInfoHandleMiddleware': 105,
    },
    'RETRY_ENABLE': True,
    'PROXY_LEVEL': 'high',
    'CLOSESPIDER_TIMEOUT': 3600 * 5.5
}


def crawl(spiderName='DefaultCrawler',
          settings=None,
          fromTask=None,
          urlList=[],
          **kwargs):
    if fromTask or urlList:
        if not urlList:
            urlList = list(map(lambda x: json.loads(
                x.decode()), dj_settings.REDIS_CACHE.smembers(kwargs['ti'].xcom_pull(task_ids=fromTask))))
        spider_call(spiderName='DefaultCrawler',
                    settings=settings,
                    urlList=urlList)


dag = DAG('NewHouseCQ', default_args=default_args,
          schedule_interval="15 */12 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseCQ',
    python_callable=crawl,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://www.cq315house.com/315web/HtmlPage/SpfQuery.htm',
                            'meta': {'PageType': 'ProjectBase'}}]},
    dag=dag)


def get_project_list(**kwargs):
    key = uuid.uuid1().hex
    r = dj_settings.REDIS_CACHE
    cur = ProjectBaseChongqing.objects
    for item in cur:
        project_info = {'source_url': item.ProjectURL,
                        'meta': {'PageType': 'ProjectInfo'}}
        r.sadd(key, json.dumps(project_info))
    r.expire(key, int(spider_settings.get('CLOSESPIDER_TIMEOUT')))
    return key


t2_cache = PythonOperator(
    task_id='LoadProjectInfoCQCache',
    python_callable=get_project_list,
    dag=dag)


t2 = PythonOperator(
    task_id='LoadProjectInfoCQ',
    python_callable=crawl,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'fromTask': 'LoadProjectInfoCQCache'},
    dag=dag)
t2.set_upstream(t2_cache)


def cacheLoader(**kwargs):
    key = uuid.uuid1().hex
    cur = BuildingInfoChongqing.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
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
    return key


t3 = PythonOperator(
    task_id='LoadBuildingInfoCache',
    python_callable=cacheLoader,
    dag=dag)

t4 = PythonOperator(
    task_id='LoadBuildingInfoCQ',
    python_callable=crawl,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'fromTask': 'LoadBuildingInfoCache'},
    dag=dag)
t4.set_upstream(t3)
