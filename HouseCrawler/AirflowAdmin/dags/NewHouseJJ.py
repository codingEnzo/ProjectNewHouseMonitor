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


default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2017, 11, 17, 15, 30),
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
                'HouseCrawler.Pipelines.PipelinesJJ.JJPipeline': 300,
                },
            'SPIDER_MIDDLEWARES': {
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJJ.ProjectBaseHandleMiddleware': 102,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJJ.ProjectInfoHandleMiddleware': 103,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJJ.BuildingListHandleMiddleware': 104,
                'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresJJ.HouseInfoHandleMiddleware': 105,
                },
            'RETRY_ENABLE': True,
            'CLOSESPIDER_TIMEOUT': 3600 * 3.5
            }

def spider_call_1(spiderName, settings, urlList):
    print(spiderName, settings, urlList)

dag = DAG('NewHouseJJ', default_args=default_args,
    schedule_interval="*/1 * * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseJJ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
              'settings': spider_settings,
              'urlList': [{'source_url': 'http://www.jjzzfdc.com.cn/WebClient/ClientService/frmSalesLPDisplay_more.aspx?qcount=10000&pcount=10000&Page=1',
                    'meta': {'PageType': 'ProjectBase'}}]},
    dag=dag)

# t2 = PythonOperator(
#     task_id='LoadProjectInfoJJ',
#     python_callable='date',
#     dag=dag)

# t3 = PythonOperator(
#     task_id='LoadProjectBaseJJ',
#     python_callable='date',
#     dag=dag)
