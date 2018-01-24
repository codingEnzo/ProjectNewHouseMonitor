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
        # 'HouseCrawler.Pipelines.PipelinesXuzhou.ImageFilePipeline': 299,
        'HouseCrawler.Pipelines.PipelinesXuzhou.PipelineXuzhou': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.ProjectBaseHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.ProjectInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.PresellInfoHandleMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.BuildingInfoHandleMiddleware': 107,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXuzhou.HouseInfoHandleMiddleware': 108,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    },
    'POST_DEFAULT_REQUEST_HEADERS': {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.xzhouse.com.cn',
        'Content-Type': 'application/json;charset=UTF-8',
    },
    'USER_AGENTS':[
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    ],
    'FILES_STORE':'/tmp',
    'FILES_EXPIRES':30,
}

dag = DAG('NewHouseXuzhou', default_args=default_args, schedule_interval="20 */8 * * *")


project_base_list = []
DistrictNames = ['云龙区', '泉山区', '经济开发区', '贾汪区', '铜山区']
for DistrictName in DistrictNames:
    param = "{'CurrentPageIndex':0,'whereContent':'I_Dist|" + DistrictName + "'}"
    project_base = {
        'source_url': 'http://www.xzhouse.com.cn/xlxx.aspx/GridBind',
        'body': param,
        'use_urlencode':False,
        'method': 'POST',
        'meta': {
            'PageType': 'ProjectBase',
            'GetPage': True,
            'DistrictName': DistrictName
        }
    }
    project_base_list.append(project_base)

index_base = {
    'source_url': 'http://www.xzhouse.com.cn/xlxx.aspx',
    'meta': {
        'PageType': 'ProjectBaseLoad',
    }
}
project_base_list.append(index_base)

t1 = PythonOperator(
    task_id='LoadProjectBaseXuzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': project_base_list
    },
    dag=dag
)



cur = BuildingInfoXuzhou.objects.all()
houseList_info_list = []
for item in cur:
    if item['CurTimeStamp'] >= str(datetime.datetime.now().date()):
        houseList_info = {'source_url': item['SourceUrl'],
                          'meta': {'PageType': 'HouseList',
                                   'PresellUUID': str(item['PresellUUID']),
                                   'ProjectUUID': str(item['ProjectUUID']),
                                   'ProjectName': item['ProjectName'],
                                   'BuildingName': item['BuildingName'],
                                   'BuildingUUID': str(item['BuildingUUID']),
                                   }
                          }
        houseList_info_list.append(houseList_info)


t2 = PythonOperator(
    task_id='LoadHouseListXuzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': houseList_info_list
    },
    dag=dag
)