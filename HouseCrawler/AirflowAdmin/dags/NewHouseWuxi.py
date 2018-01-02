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

from HouseNew.models import MonitorProjectBaseWuxi,MonitorHouseBaseWuxi
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
      'HouseCrawler.Pipelines.PipelinesWuxi.Pipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
      'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuxi.SpiderMiddlerProjectBase': 101,
      'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuxi.SpiderMiddlerBuildingBase': 102,
      'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuxi.SpiderMiddlerDeveloperBase': 103,
      'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuxi.SpiderMiddlerHouseBase': 104,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
}

dag = DAG('NewHouseWuxi', default_args=default_args, schedule_interval="40 */8 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseWuxi',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [
            {
                'source_url': 'http://www.wxhouse.com:9097/wwzs/getzxlpxx.action',
                'meta': {'PageType': 'ProjectStart'}
            }            
        ],
        'spider_count': 10
    },
    dag=dag
)

project_info_list = []
headers = {
            'User-Agent':random.choice(setting.USER_AGENTS),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'no-cache',
            'Connection': 'keep - alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.wxhouse.com:9097',
        }
cur = MonitorProjectBaseWuxi.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                         {'$group':
                                             {'_id': "$ProjectNo",
                                              'CurTimeStamp':{'$last': '$CurTimeStamp'},
                                              'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                              'change_data': {'$last': '$change_data'},
                                              'projectDetailUrl':{'$last': '$projectDetailUrl'},
                                              'ProjectCode': {'$last': '$ProjectCode'},
                                             }
                                         }],allowDiskUse=True)

num = 0
for item in cur:
    change_data = item['change_data']
    projectDetailUrl = item['projectDetailUrl']
    if projectDetailUrl and change_data != "last" and change_data != "":
        res_object = MonitorProjectBaseWuxi.objects.filter(ProjectNo=item['_id']).latest(field_name='CurTimeStamp')
        res_object.change_data = "last"
        res_object.save()
        ProjectCode = item['ProjectCode']
        projectInfo = {'source_url': item['projectDetailUrl'],
                       'meta': {
                           'PageType': 'ProjectInfo',
                           'ProjectHref': ProjectCode
                       }
                       }     
        project_info_list.append(projectInfo)
t2 = PythonOperator(
    task_id='LoadProjectInfoWuxi',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list,
               'spider_count': 10},
    dag=dag
)

house_info_list = []
cur = MonitorHouseBaseWuxi.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                             {'$group':
                                                  {'_id': "$HouseNo",
                                                   'CurTimeStamp': {'$last': '$CurTimeStamp'},
                                                   'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                                   'change_data': {'$last': '$change_data'},
                                                   'HouseInfoUrl': {'$last': '$HouseInfoUrl'},
                                                   'ProjectName': {'$last': '$ProjectName'},
                                                   'BuildingNum': {'$last': '$BuildingNum'},
                                                   'SourceUrl': {'$last': '$SourceUrl'},
                                                   }
                                              },
                                          ],allowDiskUse=True)
for item in cur:
    change_data = item['change_data']
    HouseInfoUrl = item['HouseInfoUrl']
    HouseNo = item['_id']
    ProjectName = item['ProjectName']
    BuildingNum = item['BuildingNum']
    SourceUrl = item['SourceUrl']
    if change_data != "last":
        res_object = MonitorHouseBaseWuxi.objects.filter(HouseNo=item['_id']).latest(field_name='CurTimeStamp')
        res_object.change_data = "last"
        res_object.save()
        headers['Referer'] = SourceUrl
        houseInfo = {'source_url': HouseInfoUrl,
                       'headers': headers,
                       'method': 'GET',
                       'meta': {
                           'PageType': 'HouseBase',
                           'ProjectName': ProjectName,
                           'BuildingNum': BuildingNum,
                           'houseNo': HouseNo,
                       }
                       }
        house_info_list.append(houseInfo)

t3 = PythonOperator(
    task_id='LoadHouseInfoWuxi',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': house_info_list,
               'spider_count': 10
               },
    dag=dag)
