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

from HouseNew.models import ProjectBaseZhaoqing, BuildingInfoZhaoqing
from services.spider_service import spider_call

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=9)

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
        'HouseCrawler.Pipelines.PipelinesZQ.ZQPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZQ.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZQ.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZQ.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZQ.HouseInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZQ.CompanyInfoHandleMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresZQ.PreSellInfoHandleMiddleware': 107,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.5,
    'CONCURRENT_REQUESTS': 8,
    'RETRY_TIMES': 30
}

dag = DAG('NewHouseZQ', default_args=default_args,
          schedule_interval="15 */6 * * *")

project_base_urls = ['http://www.zqjs.gov.cn/Housepresell/user_kfs.aspx?lid=1db4a74a-946d-4d8c-868d-af15a23b2ff3',
                     'http://www.zqjs.gov.cn/Housepresell/user_kfs.aspx?lid=f96ea453-7c8f-488c-beb4-a696849bba06',
                     'http://www.zqjs.gov.cn/Housepresell/user_kfs.aspx?lid=a0dd416b-ab92-49cd-ad3b-43cabc8d9486',
                     'http://www.zqjs.gov.cn/Housepresell/user_kfs.aspx?lid=75edcefe-ed69-4ee0-99c8-1d490faf7d8c',
                     'http://www.zqjs.gov.cn/Housepresell/user_kfs.aspx?lid=87372051-2f41-4972-b7f6-cb536e7fbed0',
                     'http://www.zqjs.gov.cn/Housepresell/user_kfs.aspx?lid=68ffd485-47e3-40b5-9874-d34892587390',
                     'http://www.zqjs.gov.cn/Housepresell/user_kfs.aspx?lid=52f3f3cc-68a0-46dd-92a3-1fb39e36184e']
project_base_list = []
for url in project_base_urls:
    project_base = {'source_url': url,
                    'meta': {'PageType': 'ProjectBase'}}
    project_base_list.append(project_base)
t1 = PythonOperator(
    task_id='LoadProjectBaseZQ',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': project_base_list},
    dag=dag
)

project_info_list = []
cur = ProjectBaseZhaoqing.objects.all()
for item in cur:
    project_info = {'source_url': item.ProjectURL,
                    'meta': {'PageType': 'ProjectInfo'}}
    project_info_list.append(project_info)
t2 = PythonOperator(
    task_id='LoadProjectInfoZQ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list,
               'spider_count': 16},
    dag=dag
)

building_info_list = []
cur = BuildingInfoZhaoqing.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
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

index_skip = int(math.ceil(len(building_info_list) / float(2))) + 1
for cur, index in enumerate(list(range(0, len(building_info_list), index_skip))):
    t3 = PythonOperator(
        task_id='LoadBuildingInfoZQ_%s' % cur,
        python_callable=spider_call,
        op_kwargs={'spiderName': 'DefaultCrawler',
                   'settings': spider_settings,
                   'urlList': building_info_list[index:index + index_skip]},
        dag=dag)
