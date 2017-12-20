# -*-coding=utf-8-*-
import datetime
import functools
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
        'HouseCrawler.Pipelines.PipelinesHZ.HZPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.IndexInfoHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.ProjectBaseHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.TemplateInfoHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.ProjectInfoHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.PresellListHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.PresellAPIHandleMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.BuildingListHandleMiddleware': 107,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.TemplateHouseListHandleMiddleware': 108,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.HouseListHandleMiddleware': 109,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresHZ.HouseInfoHandleMiddleware': 109,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
}

dag = DAG('NewHouseHZ', default_args=default_args,
          schedule_interval="25 */8 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseHZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://www.tmsf.com/newhouse/property_searchall.htm?sid=&districtid=',
                            'meta': {'PageType': 'ProjectBase', 'curPage': 1}}]},
    dag=dag)

project_info_list = []

cur = ProjectBaseHangzhou.objects.aggregate(*[
    {"$sort":
        {
            "CurTimeStamp": 1
        }},
    {
        '$match': {
            'OnSaleState': {
                '$ne': '售完'
            }
        }
    }, {'$group':
        {
            '_id': "$ProjectUUID",
            'ProjectName': {'$first': '$ProjectName'},
            'sid': {'$first': '$sid'},
            'PropertyID': {'$first': '$PropertyID'},
            'RegionName': {'$first': '$RegionName'},
            'SourceUrl': {'$first': '$SourceUrl'},
            'OnSaleState': {'$first': '$OnSaleState'},
        }}
])
for item in cur:
    project_info = {'source_url': item['SourceUrl'],
                    'meta': {
                        'PageType': 'MonitProjectInfo',
                        'sid': item['sid'],
                        'PropertyID': item['PropertyID'],
                        'RegionName': item['RegionName'],
                    }}
    project_info_list.append(project_info)

t2 = PythonOperator(
    task_id='MonitProjectInfoHZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_list},
    dag=dag
)

index_base = {
    'source_url': 'http://www.tmsf.com/index.jsp',
    'meta': {'PageType': 'IndexInfo'}}

t3 = PythonOperator(
    task_id='LoadIndexInfoHZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [index_base, ]},
    dag=dag
)
