# -*-coding=utf-8-*-
import datetime
import functools
import os
import sys

import django
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
}

dag = DAG('NewHouseFS', default_args=default_args, schedule_interval='10 */7.5 * * *')

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
cur = BuildingDetailFoshan.objects.all()
for item in cur:
    source_url = "http://fsfc.fsjw.gov.cn/hpms_project/room.jhtml?id={0}".format(item.BuildingID)
    building_detail = {
        'source_url': source_url,
        'method': 'GET',
        'meta': {
            'PageType': 'hd_url',
            'Record_Data': {
                "Crawler_type": 'ini',
                "ProjectName": item.ProjectName,
                "RegionName": item.RegionName,
                'BuildingName': item.BuildingName,
                'BuildingUUID': str(item.BuildingUUID),
                "ProjectUUID": str(item.ProjectUUID),
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

house_detail_list = []
cur = HouseDetailFoshan.objects.filter(ComplateTag=0)
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
    house_detail_list.append(house_detail)

t3 = PythonOperator(
    task_id='LoadHouseDetailFS',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': house_detail_list
    },
    dag=dag
)

t4 = PythonOperator(
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
    }
)
