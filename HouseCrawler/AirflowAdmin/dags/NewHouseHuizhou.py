# -*-coding=utf-8-*-
import datetime
import functools
import json
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
        "HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHuizhou.ProjectListMiddleware": 102,
        "HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHuizhou.ProjectDetailMiddleware": 103,
        "HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHuizhou.BuildingDetailMiddleware": 104,
        "HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHuizhou.CertificateDetailMiddleware": 105,
        "HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHuizhou.HouseDetailMiddleware": 106,
        "HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHuizhou.MonitorMiddleware": 107,
    },
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesHuizhou.PipelineHuizhou': 300,
    },
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware': None,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
}

dag = DAG('NewHouseHuizhou', default_args=default_args, schedule_interval='10 */8 * * *')

t1 = PythonOperator(
    task_id='LoadProjectDetaiHuizhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [{
            'source_url': "http://newhouse.fz0752.com/project/list.shtml?state=&key=&qy=&area=&danjia=&func=&fea=&type=&kp=&mj=&pageNO=1",
            'meta': {'PageType': 'pl_url'}
        }]
    },
    dag=dag
)

building_detail_list = []
cur = Project_DetailHuizhou.objects.aggregate(*[
        {
            '$sort':{'RecordTime':-1}
        },
        {
            '$group':{'_id':'$ProjectUUID',
                      'ProjectUUID':{'$first':'$ProjectUUID'},
                      'ProjectName':{'$first':'$ProjectName'},
                      'ProjectID':{'$first':'$ProjectID'},
                      'RegionName':{'$first':'$RegionName'},
                      'RealEstateProjectID':{'$first':'$RealEstateProjectID'},
            }
        }
    ])

for item in cur:
    if item['RealEstateProjectID']:
        building_detail = {
            'source_url': 'http://newhouse.fz0752.com/project/selist.shtml?num={0}'.format(item['RealEstateProjectID']),
            'method': 'GET',
            'meta': {
                'PageType': 'bd_url',
                'Record_Data': {
                    "ProjectUUID": str(item['ProjectUUID']),
                    "ProjectName": item['ProjectName'],
                    "ProjectID": item['ProjectID'],
                    "RegionName": item['RegionName'],
                }
            }
        }
        building_detail_list.append(building_detail)

t2 = PythonOperator(
    task_id='LoadBuildinglHuizhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': building_detail_list
    },
    dag=dag
)

def cache_query():
    r = dj_settings.REDIS_CACHE
    cur = Building_DetailHuizhou.objects.aggregate(*[{'$sort': {'CheackTimeLatest': -1}},
                                                     {'$group': {'_id': '$BuildingUUID',
                                                                 'ProjectUUID': {'$first': '$ProjectUUID'},
                                                                 'BuildingUUID': {'$first': '$BuildingUUID'},
                                                                 'PresalePermitNumberUUID': {
                                                                     '$first': '$PresalePermitNumberUUID'},
                                                                 'ProjectName': {'$first': '$ProjectName'},
                                                                 'BuildingName': {'$first': '$BuildingName'},
                                                                 'BuildingNumber': {'$first': '$BuildingNumber'},
                                                                 'CheackTimeLatest': {'$first': '$CheackTimeLatest'},
                                                                 'BuildingUrl': {'$first': '$BuildingUrl'}}}
                                                     ])
    for item in cur:
        try:
            if item['BuildingUrl']:
                house_detail = {'source_url': item['BuildingUrl'],
                                'method': 'GET',
                                'meta': {
                                    'PageType': 'hd_url',
                                    'Record_Data': {
                                        "ProjectUUID": str(item['ProjectUUID']),
                                        "BuildingUUID": str(item['BuildingUUID']),
                                        "PresalePermitNumberUUID": str(item['PresalePermitNumberUUID']),
                                        "ProjectName": item['ProjectName'],
                                        "BuildingName": item['BuildingName'],
                                        'BuildingNumber': item['BuildingNumber'],
                                        'Fidfailtime': 0
                                    }
                                }
                                }
                result = json.dumps(house_detail)
                r.sadd('NewHouseHuizhou', result)
        except Exception:
            import traceback
            traceback.print_exc()
    r.expire('NewHouseHuizhou', 3600)

t3 = PythonOperator(
    task_id='LoadHouseDetailHuizhouCache',
    python_callable=cache_query,
    dag=dag
)


house_detail_list = list(map(lambda x: json.loads(x), dj_settings.REDIS_CACHE.smembers('NewHouseHuizhou')))
t4 = PythonOperator(
    task_id='LoadHouseDetailHuizhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': house_detail_list
    },
    dag=dag
)
t4.set_upstream(t3)