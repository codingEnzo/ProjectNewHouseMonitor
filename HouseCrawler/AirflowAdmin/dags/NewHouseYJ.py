# -*- coding: utf-8 -*-
import datetime
import os
import sys
import json
import math
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

from HouseNew.models import ProjectBaseYangjiang, BuildingInfoYangjiang
from services.spider_service import spider_call
from django.conf import settings as dj_settings

REDIS_CACHE_KEY = "NewHouseYJ"

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=14)

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
        'HouseCrawler.Pipelines.PipelinesYJ.YJPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYJ.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYJ.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYJ.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYJ.HouseInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYJ.CompanyInfoHandleMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYJ.PreSellInfoHandleMiddleware': 107,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYJ.ProjectIndexHandleMiddleware': 108,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.7,
    'CONCURRENT_REQUESTS': 8,
    'RETRY_TIMES': 30,
    'REDIRECT_ENABLED': True
}

dag = DAG('NewHouseYJ', default_args=default_args,
          schedule_interval="15 */12 * * *")

project_base_urls = ['http://219.129.189.12:8090/JHHouseWeb/user_kfs.aspx?lid=a88b3b89-472c-493b-9b4b-970f7848114f',
                     'http://219.129.189.12:8090/JHHouseWeb/user_kfs.aspx?lid=c4407134-22b9-4a2e-9556-9df063088aca',
                     'http://219.129.189.12:8090/JHHouseWeb/user_kfs.aspx?lid=caf441f1-a969-4682-8e63-4586ffe5caa8',
                     'http://219.129.189.12:8090/JHHouseWeb/user_kfs.aspx?lid=fefe5706-0b08-42a1-bbe6-78c5d54d4dba',
                     'http://219.129.189.12:8090/JHHouseWeb/user_kfs.aspx?lid=acf37d73-3bf0-4819-9f55-3a9279f54ab8']
project_base_list = []
for url in project_base_urls:
    project_base = {'source_url': url,
                    'meta': {'PageType': 'ProjectBase'}}
    project_base_list.append(project_base)
t1 = PythonOperator(
    task_id='LoadProjectBaseYJ',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': project_base_list},
    dag=dag
)

project_info_list = []
cur = ProjectBaseYangjiang.objects.all()
for item in cur:
    project_info = {'source_url': item.ProjectURL,
                    'meta': {'PageType': 'ProjectInfo'}}
    project_info_list.append(project_info)
t2 = PythonOperator(
    task_id='LoadProjectInfoYJ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list,
               'spider_count': 16},
    dag=dag
)


def cacheLoader(key=REDIS_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    cur = BuildingInfoYangjiang.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
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
        task_id='LoadBuildingInfoYJ_%s' % cur,
        python_callable=spider_call,
        op_kwargs={'spiderName': 'DefaultCrawler',
                   'settings': spider_settings,
                   'urlList': building_info_list[index:index + index_skip],
                   'spider_count': 32},
        dag=dag)
    t4.set_upstream(t3)
