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


STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=6)

default_args = {
    'owner': 'airflow',
    'start_date': STARTDATE,
    'email': ['1012137875@qq.com'],
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
                'HouseCrawler.Pipelines.PipelinesHF.HFPipeline': 300,
                },
            'SPIDER_MIDDLEWARES': {
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHF.ProjectBaseHandleMiddleware': 102,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHF.ProjectInfoHandleMiddleware': 103,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHF.BuildingListHandleMiddleware': 104,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHF.HouseInfoHandleMiddleware': 105,
                },
            'RETRY_ENABLE': True,
            'CLOSESPIDER_TIMEOUT': 3600 * 3.5
            }


dag = DAG('NewHouseHF', default_args=default_args,
            schedule_interval="25 */4 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseHF',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
              'settings': spider_settings,
              'urlList': [{'source_url': 'http://real.hffd.gov.cn/',
                    'meta': {'PageType': 'ProjectBase'}}]},
    dag=dag)


builfing_info_list = []
cur = BuildingInfoGuiyang.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                             {'$group':
                                                 {'_id': "$BuildingUUID",
                                                  'ProjectName': {'$first': '$ProjectName'},
                                                  'ProjectUUID': {'$first': '$ProjectUUID'},
                                                  'BuildingName': {'$first': '$BuildingName'},
                                                  'BuildingUUID': {'$first': '$BuildingUUID'},
                                                  'BuildingURL': {'$first': '$BuildingURL'},
                                                 }
                                             }])

for item in cur:
    try:
        if item['BuildingURL']:
            if True:
                builfing_info = {'source_url': item['BuildingURL'],
                                    'meta': {'PageType': 'HouseInfo',
                                                'ProjectName': item['ProjectName'],
                                                'BuildingName': item['BuildingName'],
                                                'ProjectUUID': str(item['ProjectUUID']),
                                                'BuildingUUID': str(item['BuildingUUID'])}}
                builfing_info_list.append(builfing_info)
    except Exception:
        import traceback
        traceback.print_exc()
t2 = PythonOperator(
    task_id='LoadBuildingInfoHF',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
                  'settings': spider_settings,
                  'urlList': builfing_info_list},
    dag=dag)
