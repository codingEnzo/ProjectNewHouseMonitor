# -*- coding: utf-8 -*-
import datetime
import os
import sys

import django
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

BASE_DIR = os.path.abspath(os.environ.get('AIRFLOW_HOME'))
HOUSESERVICECORE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore'))
HOUSEADMIN_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore/HouseAdmin'))
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

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=6)

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
        'HouseCrawler.Pipelines.PipelinesCS.CSPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCS.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCS.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCS.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCS.HouseInfoHandleMiddleware': 105,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 3.6,
    'CONCURRENT_REQUESTS': 64,
}

dag = DAG('NewHouseCS', default_args=default_args, schedule_interval="15 */4 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseCS',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [
            {'source_url': 'http://search.csfdc.gov.cn/index.php/home/Index/sfloor',
             'meta': {'PageType': 'ProjectBase'}}
        ]
    },
    dag=dag
)

project_info_list = []
cur = ProjectBaseChangsha.objects.all()
for item in cur:
    project_info = {'source_url': item.ProjectURL,
                    'meta': {'PageType': 'ProjectInfo'}}
    project_info_list.append(project_info)

t2 = PythonOperator(
    task_id='LoadProjectInfoCS',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list},
    dag=dag
)

building_info_list = []
cur = BuildingInfoChangsha.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                               {'$group': {
                                                   '_id': "$BuildingUUID",
                                                   'ProjectName': {'$first': '$ProjectName'},
                                                   'ProjectUUID': {'$first': '$ProjectUUID'},
                                                   'BuildingName': {'$first': '$BuildingName'},
                                                   'BuildingUUID': {'$first': '$BuildingUUID'},
                                                   'BuildingURL': {'$first': '$BuildingURL'},
                                                   'BuildingURLCurTimeStamp': {'$first': '$BuildingURLCurTimeStamp'}
                                               }}])
for item in cur:
    if item['BuildingURL']:
        if item['BuildingURLCurTimeStamp'] >= str(datetime.datetime.now().date()):
            building_info = {'source_url': item['BuildingURL'],
                             'meta': {'PageType': 'HouseInfo',
                                      'ProjectName': item['ProjectName'],
                                      'BuildingName': item['BuildingName'],
                                      'ProjectUUID': str(item['ProjectUUID']),
                                      'BuildingUUID': str(item['BuildingUUID'])}}
            building_info_list.append(building_info)

t3 = PythonOperator(
    task_id='LoadBuildingInfoCS',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': building_info_list},
    dag=dag)
