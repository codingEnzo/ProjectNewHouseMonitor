# -*- coding: utf-8 -*-
import datetime
import os
import sys
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

from HouseNew.models import ProjectBaseYunfu, BuildingInfoYunfu
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
        'HouseCrawler.Pipelines.PipelinesYF.YFPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYF.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYF.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYF.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYF.HouseInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYF.CompanyInfoHandleMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYF.PreSellInfoHandleMiddleware': 107,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresYF.ProjectIndexHandleMiddleware': 108,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.7,
    'CONCURRENT_REQUESTS': 8,
    'RETRY_TIMES': 30,
    'REDIRECT_ENABLED': True
}

dag = DAG('NewHouseYF', default_args=default_args,
          schedule_interval="15 */6 * * *")

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
    task_id='LoadProjectBaseYF',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': project_base_list},
    dag=dag
)

project_info_list = []
cur = ProjectBaseYunfu.objects.all()
for item in cur:
    project_info = {'source_url': item.ProjectURL,
                    'meta': {'PageType': 'ProjectInfo'}}
    project_info_list.append(project_info)
t2 = PythonOperator(
    task_id='LoadProjectInfoYF',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list,
               'spider_count': 16},
    dag=dag
)

building_info_list = []
cur = BuildingInfoYunfu.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                               {'$group': {
                                                   '_id': "$BuildingUUID",
                                                   'ProjectName': {'$first': '$ProjectName'},
                                                   'ProjectUUID': {'$first': '$ProjectUUID'},
                                                   'BuildingName': {'$first': '$BuildingName'},
                                                   'BuildingUUID': {'$first': '$BuildingUUID'},
                                                   'BuildingURL': {'$first': '$BuildingURL'}
                                               }}])
for item in cur:
    if item['BuildingURL']:
        if True:
            building_info = {'source_url': item['BuildingURL'],
                             'meta': {'PageType': 'HouseInfo',
                                      'ProjectName': item['ProjectName'],
                                      'BuildingName': item['BuildingName'],
                                      'ProjectUUID': str(item['ProjectUUID']),
                                      'BuildingUUID': str(item['BuildingUUID'])}}
            building_info_list.append(building_info)

index_skip = int(math.ceil(len(building_info_list) / float(4))) + 1
for cur, index in enumerate(list(range(0, len(building_info_list), index_skip))):
    t3 = PythonOperator(
        task_id='LoadBuildingInfoYF_%s' % cur,
        python_callable=spider_call,
        op_kwargs={'spiderName': 'DefaultCrawler',
                   'settings': spider_settings,
                   'urlList': building_info_list[index:index + index_skip],
                   'spider_count': 32},
        dag=dag)
