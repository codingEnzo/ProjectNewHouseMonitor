# -*-coding=utf-8-*-
import os
import sys
import django
import json
import datetime
import functools
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

BASE_DIR = os.path.abspath(os.environ.get('AIRFLOW_HOME'))
HOUSESERVICECORE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'ServiceCore'))
HOUSEADMIN_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'ServiceCore/HouseAdmin'))
HOUSECRAWLER_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'ServiceCore/HouseCrawler'))
HOUSESERVICE_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'ServiceCore/SpiderService'))

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

REDIS_CACHE_KEY = "NewHouseFZ"


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


STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=14)

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
        'HouseCrawler.Pipelines.PipelinesFZ.FZPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFZ.GetProjectPageBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFZ.GetProjectBaseHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFZ.OpenningunitBaseHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFZ.BuildingBaseHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresFZ.HouseBaseHandleMiddleware': 106,
    },
    'RETRY_ENABLE': True,
    'PROXY_ENABLE': True,
    'REDIRECT_ENABLED': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.8
}

headers = {
    'Host': '222.77.178.63:7002',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

dag = DAG('NewHouseFZ', default_args=default_args,
          schedule_interval="15 */12 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseFZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://222.77.178.63:7002/result_new.asp',
                            'meta': {'PageType': 'GetProjectBase'}}]},
    dag=dag)


def cacheLoader(key=REDIS_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    cur = ProjectinfoBaseFuzhou.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                                    {'$group':
                                                     {'_id': "$projectuuid",
                                                      'CurTimeStamp': {'$last': '$CurTimeStamp'},
                                                      'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                                      'change_data': {'$last': '$change_data'},
                                                      'Projectname': {'$last': '$Projectname'},
                                                      'ApprovalUrl': {'$last': '$ApprovalUrl'}
                                                      }
                                                     }], allowDiskUse=True)
    for item in cur:
        try:
            if item['change_data'] != 'last':
                project_base = {
                    'source_url': item['ApprovalUrl'],
                    'headers': headers,
                    'meta': {
                        'PageType': 'openingunit',
                        'projectuuid': item['_id'],
                        'Projectname': item['Projectname']
                    }
                }
                r.sadd(key, json.dumps(project_base))
        except Exception:
            import traceback
            traceback.print_exc()
        r.expire(key, int(spider_settings.get('CLOSESPIDER_TIMEOUT')))


t2 = PythonOperator(
    task_id='LoadBuildingInfoCache',
    python_callable=cacheLoader,
    op_kwargs={'key': REDIS_CACHE_KEY},
    dag=dag)


building_info_list = list(map(lambda x: json.loads(
    x.decode()), dj_settings.REDIS_CACHE.smembers(REDIS_CACHE_KEY)))
t3 = PythonOperator(
    task_id='LoadOpeningUnitFZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': building_info_list},
    dag=dag)
t3.set_upstream(t2)
