# -*-coding=utf-8-*-
import os
import sys
import django
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
        'HouseCrawler.Pipelines.PipelinesQingdao.PipelineQingdao': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQingdao.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQingdao.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQingdao.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQingdao.HouseListInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresQingdao.HouseInfoHandleMiddleware': 106,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.7,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    },
    'POST_DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware': None,
    }
}

dag = DAG('NewHouseQingdao', default_args=default_args,
          schedule_interval="0 6 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseQingdao',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'https://www.qdfd.com.cn/qdweb/realweb/fh/FhProjectQuery.jsp?page=1',
                             'meta': {'PageType': 'ProjectBase', 'curPage': 1}}]},
    dag=dag)

building_list = []
cur = PresellInfoQingdao.objects.all()
url = 'https://www.qdfd.com.cn/qdweb/realweb/fh/FhBuildingList.jsp?preid={PresellID}'
for item in cur:
    building_info = {'source_url': url.format(PresellID=item['PresellID']),
                     'meta': {
        'PageType': 'BuildingListInfo',
        'ProjectUUID': str(item['ProjectUUID']),
                         'PresellUUID': str(item['PresellUUID']),
                         'ProjectName': item['ProjectName'],
                         'PresalePermitName': item['PresalePermitName'],
    }}
    building_list.append(building_info)
t2 = PythonOperator(
    task_id='LoadBuildingListQingdao',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': building_list},
    dag=dag)

builfing_info_list = []
cur = BuildingInfoQingdao.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
                                              {'$group':
                                               {'_id': "$BuildingUUID",
                                                'ProjectName': {'$first': '$ProjectName'},
                                                'ProjectUUID': {'$first': '$ProjectUUID'},
                                                'PresalePermitName': {'$first': '$PresalePermitName'},
                                                'PresellUUID': {'$first': '$PresellUUID'},
                                                'BuildingName': {'$first': '$BuildingName'},
                                                'BuildingUUID': {'$first': '$BuildingUUID'},
                                                'BuildingURL': {'$first': '$BuildingURL'},
                                                }
                                               }])

for item in cur:
    try:
        if item['BuildingURL']:
            builfing_info = {'source_url': item['BuildingURL'],
                             'meta': {'PageType': 'HouseListInfo',
                                      'ProjectName': item['ProjectName'],
                                      'PresalePermitName': item['PresalePermitName'],
                                      'BuildingName': item['BuildingName'],
                                      'ProjectUUID': str(item['ProjectUUID']),
                                      'PresellUUID': str(item['PresellUUID']),
                                      'BuildingUUID': str(item['BuildingUUID'])}}
            builfing_info_list.append(builfing_info)
    except Exception:
        import traceback
        traceback.print_exc()
t3 = PythonOperator(
    task_id='LoadHouseListQingdao',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': builfing_info_list},
    dag=dag)
