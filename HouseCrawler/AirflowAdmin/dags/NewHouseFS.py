# -*-coding=utf-8-*-
import datetime
import functools
import os
import sys
import pickle

import django
import json
import math
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
from django.conf import settings as dj_settings


def just_one_instance(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        import socket
        try:
            global s
            s = socket.socket()
            host = socket.gethostname()
            s.bind((host, 60223))
        except Exception:
            print('already has an instance')
            return None
        return func(*args, **kwargs)

    return f


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
    'SPIDER_MIDDLEWARES': {
        "HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFS.ProjectListMiddleware": 115,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFS.ProjectDetailMiddleware': 110,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFS.CertificateDetailMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFS.HouseDetailMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFS.BuildingDetailMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFS.MonitorMiddleware': 100
    },
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesFS.FSPipeline': 300,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
    'DEFAULT_REQUEST_HEADERS': {
        "Referer":"http://fsfc.fsjw.gov.cn/",
        "Host":"fsfc.fsjw.gov.cn",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
    },
}

dag = DAG('NewHouseFS', default_args=default_args, schedule_interval='10 */8 * * *')

t1 = PythonOperator(
    task_id='LoadProjectInfoFS',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [{
            'source_url': "http://fsfc.fsjw.gov.cn/search/index.do?ys=0&od=-SORT;-STIME;-LASTMODIFYTIME;RELEVANCE",
            'meta': {'PageType': 'pl_url', 'Record_Data': {'crawler_type': 'ini', 'pages_num': 1}}
        }]
    },
    dag=dag
)

building_detail_list = []
cur = BuildingDetailFoshan.objects.aggregate(*[
        {
            '$sort':{'RecordTime':-1}
        },
        {
            '$group':{'_id':'$BuildingUUID',
                      'ProjectName':{'$first':'$ProjectName'},
                      'RegionName':{'$first':'$RegionName'},
                      'BuildingName':{'$first':'$BuildingName'},
                      'BuildingUUID':{'$first':'$BuildingUUID'},
                      'ProjectUUID':{'$first':'$ProjectUUID'},
                      'BuildingID':{'$first':'$BuildingID'},
            }
        }
    ])

for item in cur:
    source_url = "http://fsfc.fsjw.gov.cn/hpms_project/room.jhtml?id={0}".format(item['BuildingID'])
    building_detail = {
        'source_url': source_url,
        'method': 'GET',
        'meta': {
            'PageType': 'hd_url',
            'Record_Data': {
                "ProjectName": item['ProjectName'],
                "RegionName": item['RegionName'],
                'BuildingName': item['BuildingName'],
                'BuildingUUID': str(item['BuildingUUID']),
                "ProjectUUID": str(item['ProjectUUID']),
                'Fidfailtime': 0
            }
        }
    }
    building_detail_list.append(building_detail)

index_skip = int(math.ceil(len(building_detail_list) / float(4))) + 1
for cur, index in enumerate(list(range(0, len(building_detail_list), index_skip))):
    t2 = PythonOperator(
        task_id='LoadBuildingDetailFS_{}'.format(cur),
        python_callable=spider_call,
        op_kwargs={
            'spiderName': 'DefaultCrawler',
            'settings': spider_settings,
            'urlList': building_detail_list[index:index + index_skip]
        },
        dag=dag
    )


def cache_query():
    cur = HouseDetailFoshan.objects.filter(ComplateTag=0)
    r = dj_settings.REDIS_CACHE
    for item in cur:
        item2 = {i: str(item[i]) for i in item}
        source_url = item2['HouseUrl']
        house_detail = {
            'source_url': source_url,
            'method': 'GET',
            'meta': {
                'PageType': 'hd_url2',
                'Item': item2
            }
        }
        result = pickle.dumps(house_detail) 
        r.sadd('NewHouseFS', result)
    r.expire('NewHouseFS', 3600)


t3 = PythonOperator(
    task_id='LoadHouseDetailFSCache',
    python_callable=cache_query,
    dag=dag
)


house_detail_list = map(lambda x: json.loads(x), dj_settings.REDIS_CACHE.smembers('NewHouseFS'))
t4 = PythonOperator(
    task_id='LoadHouseDetailFS',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': house_detail_list
    },
    dag=dag
)
t4.set_upstream(t3)


t5 = PythonOperator(
    task_id='LoadMonitorFS',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [{'source_url': "http://fsfc.fsjw.gov.cn/main/index.jhtml",
                     'method': 'GET',
                     'meta': {'PageType': 'monitor',
                              'Record_Data': {'crawler_type': 'ini',
                                              'pages_num': 1}
                              }
                     }, ]
    },
    dag=dag
)
