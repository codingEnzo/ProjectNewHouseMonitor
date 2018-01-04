# -*- coding: utf-8 -*-
import datetime
import os
import sys
import requests
import re
import random

import django
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

BASE_DIR = os.path.abspath(os.environ.get('AIRFLOW_HOME'))
HOUSESERVICECORE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore'))
HOUSEADMIN_DIR = os.path.abspath(os.path.join(BASE_DIR,'ServiceCore/HouseAdmin'))
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
    'owner': 'sun',
    'start_date': STARTDATE,
    'email': ['jiajia.sun@yunfangdata.com'],
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
    'HouseCrawler.Pipelines.PipelinesFuzhou.Pipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFuzhou.GetProjectBaseHandleMiddleware': 101,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFuzhou.GetProjectPageBaseHandleMiddleware': 102,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFuzhou.OpenningunitBaseHandleMiddleware': 103,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFuzhou.BuildingBaseHandleMiddleware': 104,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFuzhou.HouseBaseHandleMiddleware': 105,
    },
    'DOWNLOAD_FAIL_ON_DATALOSS' : False,
    'RETRY_ENABLE': False,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'RETRY_TIMES': 15,
    'CONCURRENT_REQUESTS': 64,
}

dag = DAG(
    'NewHouseFuzhou',
    default_args=default_args,
    schedule_interval="10 */5 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseFuzhou',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://222.77.178.63:7002/result_new.asp',
                            'meta': {'PageType': 'GetProjectBase'}}]},
    dag=dag
)


project_info_list = []
headers = {
            'Host': '222.77.178.63:7002',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
}

cur = ProjectinfoBaseFuzhou.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                      {'$group':
                                           {'_id': "$projectuuid",
                                            'CurTimeStamp': {'$last': '$CurTimeStamp'},
                                            'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                            'change_data': {'$last': '$change_data'},                                  
                                            'Projectname': {'$last': '$Projectname'}, 
                                            'ApprovalUrl':{'$last': '$ApprovalUrl'}                                         
                                            }
                                       }], allowDiskUse=True)
for item in cur:
      if item['change_data'] != 'last':
          res_object = ProjectinfoBaseFuzhou.objects.filter(projectuuid=item['_id']).latest(field_name='CurTimeStamp')
          res_object.change_data = "last"
          res_object.save()
          project_base = {
              'source_url': item['ApprovalUrl'],
              'headers': headers,
              'meta': {
                  'PageType': 'openingunit',
                  'projectuuid': item['_id'],
                  'Projectname': item['Projectname']
              }
          }
          project_info_list.append(project_base)


t2 = PythonOperator(
    task_id='LoadBuildingInfoFuzhou',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list,
               'spider_count': 30
               },
    dag=dag)
