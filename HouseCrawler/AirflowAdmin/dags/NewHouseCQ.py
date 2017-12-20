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


STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=8)

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
                'HouseCrawler.Pipelines.PipelinesCQ.CQPipeline': 300,
                },
            'SPIDER_MIDDLEWARES': {
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCQ.ProjectBaseHandleMiddleware': 102,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCQ.BuildingListHandleMiddleware': 104,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCQ.HouseInfoHandleMiddleware': 105,
                },
            'RETRY_ENABLE': True,
            'PROXY_LEVEL': 'high',
            'CLOSESPIDER_TIMEOUT': 3600 * 5.5
            }


dag = DAG('NewHouseCQ', default_args=default_args,
            schedule_interval="10 */6 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseCQ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
              'settings': spider_settings,
              'urlList': [{'source_url': 'http://www.cq315house.com/315web/HtmlPage/SpfQuery.htm',
                    'meta': {'PageType': 'ProjectBase'}}]},
    dag=dag)

project_info_list = []
cur = ProjectBaseChongqing.objects.all()
for item in cur:
    project_info = {'source_url': item.ProjectURL,
                    'meta': {'PageType': 'ProjectInfo'}}
    project_info_list.append(project_info)
t2 = PythonOperator(
    task_id='LoadProjectInfoCQ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
                  'settings': spider_settings,
                  'urlList': project_info_list},
    dag=dag)

builfing_info_list = []
cur = BuildingInfoChongqing.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
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
t3 = PythonOperator(
    task_id='LoadBuildingInfoCQ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
                  'settings': spider_settings,
                  'urlList': builfing_info_list},
    dag=dag)