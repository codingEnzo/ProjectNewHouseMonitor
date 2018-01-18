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

from HouseNew.models import ProjectBaseHeyuan, BuildingInfoHeyuan
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
        'HouseCrawler.Pipelines.PipelinesHY.HYPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHY.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHY.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHY.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHY.HouseInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHY.CompanyInfoHandleMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHY.PreSellInfoHandleMiddleware': 107,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.5,
    'CONCURRENT_REQUESTS': 8,
    'RETRY_TIMES': 30,
    'REDIRECT_ENABLED': True
}

dag = DAG('NewHouseHY', default_args=default_args,
          schedule_interval="0 */6 * * *")

project_base_urls = ['http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?Jgid=FC830662-EA75-427C-9A82-443B91E383CB&PageIndex=1&PageSize=5000&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc=',
                     'http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?Jgid=289e2e6c-ac49-43ba-be2a-eaf6060d615b&PageIndex=1&PageSize=5000&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc=',
                     'http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?Jgid=b5bd0991-9a19-4bfb-a27d-6562e469eb73&PageIndex=1&PageSize=5000&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc=',
                     'http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?Jgid=172df23b-1b15-47ba-b8ff-fd1e4f68c6db&PageIndex=1&PageSize=5000&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc=',
                     'http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?Jgid=0a3257dd-774b-40e0-93a1-521d0a8cf602&PageIndex=1&PageSize=5000&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc=',
                     'http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?Jgid=ddb2f53f-1d25-4732-a244-ffaec88c3c49&PageIndex=1&PageSize=5000&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc=']
project_base_list = []
for url in project_base_urls:
    project_base = {'source_url': url,
                    'meta': {'PageType': 'ProjectBase'}}
    project_base_list.append(project_base)
t1 = PythonOperator(
    task_id='LoadProjectBaseHY',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': project_base_list},
    dag=dag
)

project_info_list = []
cur = ProjectBaseHeyuan.objects.all()
for item in cur:
    project_info = {'source_url': item.ProjectURL,
                    'meta': {'PageType': 'ProjectInfo'}}
    project_info_list.append(project_info)
t2 = PythonOperator(
    task_id='LoadProjectInfoHY',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list,
               'spider_count': 16},
    dag=dag
)

building_info_list = []
cur = BuildingInfoHeyuan.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
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
        task_id='LoadBuildingInfoHY_%s' % cur,
        python_callable=spider_call,
        op_kwargs={'spiderName': 'DefaultCrawler',
                   'settings': spider_settings,
                   'urlList': building_info_list[index:index + index_skip],
                   'spider_count': 32},
        dag=dag)
