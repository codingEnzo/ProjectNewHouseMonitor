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
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.7,
    'CONCURRENT_REQUESTS': 8,
    'RETRY_TIMES': 30,
    'REDIRECT_ENABLED': True
}

spider_index_settings = {
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesYF.YFPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
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

dag_index = DAG('NewHouseYF_Index', default_args=default_args,
          schedule_interval="15 23 * * *")

project_base_urls = ['http://www.yfci.gov.cn:8080/HousePresell/user_kfs_old.aspx?lid=4940be08-edc0-4792-a0b5-1ee518530651&page=1',
                     'http://www.yfci.gov.cn:8080/HousePresell/user_kfs_old.aspx?lid=b2fe0e00-f601-4748-9b9e-1475a3ef0085&page=1',
                     'http://www.yfci.gov.cn:8080/HousePresell/user_kfs_old.aspx?lid=71ffcc09-ac55-4960-be3c-56a7bbe06804&page=1',
                     'http://www.yfci.gov.cn:8080/HousePresell/user_kfs_old.aspx?lid=ded72eac-dd4f-4675-a044-301bf2b337a5&page=1',
                     'http://www.yfci.gov.cn:8080/HousePresell/user_kfs_old.aspx?lid=bfb9bd7b-6468-469e-b3e7-e8498d6a2ecc&page=1']
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

t1_index = PythonOperator(
    task_id='LoadProjectBaseYF_index',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_index_settings,
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
