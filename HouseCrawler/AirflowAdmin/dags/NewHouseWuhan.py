# -*-coding=utf-8-*-
import os
import pickle
import sys
import json
import django
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

REDIS_BUILDING_CACHE_KEY = "NewHouseWuhan_BuildingList"
REDIS_HOUSE_CACHE_KEY = "NewHouseWuhan_HouseList"


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
        'HouseCrawler.Pipelines.PipelinesWuhan.WuhanPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuhan.ProjectListHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuhan.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuhan.BuildingListHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresWuhan.HouseListHandleMiddleware': 105,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.8,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'fgj.wuhan.gov.cn',
    },
    'POST_DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'fgj.wuhan.gov.cn',
    }
}

dag = DAG('NewHouseWuhan', default_args=default_args,
          schedule_interval="15 */12 * * *")

t1 = PythonOperator(
    task_id='LoadProjectInfoWuhan',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://fgj.wuhan.gov.cn/zz_spfxmcx_index.jspx',
                            'meta': {'PageType': 'ProjectList'}}]},
    dag=dag)


def query_mongodb(name="BuildingList", key=REDIS_BUILDING_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    try:

        if name == 'BuildingList':
            cur = ProjectInfoWuhan.objects.aggregate(*[
                {'$group':
                     {'_id': "$ProjectUUID",
                      'RealEstateProjectID': {'$first': '$RealEstateProjectID'},
                      'ProjectUUID': {'$first': '$ProjectUUID'},
                      'ProjectName': {'$first': '$ProjectName'},
                      }
                 }
            ])
            for item in cur:

                if item['RealEstateProjectID']:
                    url = 'http://fgj.wuhan.gov.cn/zz_spfxmcx_loupan.jspx?dengJh={id}'.format(
                        id=item['RealEstateProjectID'])
                    buildingList_info = {'source_url': url,
                                         'meta': {
                                             'PageType': 'BuildingList',
                                             'ProjectUUID': str(item['ProjectUUID']),
                                             'ProjectName': str(item['ProjectName'])
                                         }}
                    r.sadd(key, pickle.dumps(buildingList_info))
        elif name == 'HouseList':
            cur = BuildingInfoWuhan.objects.aggregate(*[
                {'$group':
                     {'_id': "$BuildingUUID",
                      'ProjectUUID': {'$first': '$ProjectUUID'},
                      'ProjectName': {'$first': '$ProjectName'},
                      'BuildingUUID': {'$first': '$BuildingUUID'},
                      'BuildingName': {'$first': '$BuildingName'},
                      'SourceUrl': {'$first': '$SourceUrl'},
                      }
                 }
            ])
            for item in cur:
                houseList_info = {'source_url': item['SourceUrl'],
                                  'meta': {
                                      'PageType': 'HouseList',
                                      'ProjectUUID': str(item['ProjectUUID']),
                                      'ProjectName': str(item['ProjectName']),
                                      'BuildingUUID': str(item['BuildingUUID']),
                                      'BuildingName': str(item['BuildingName']),
                                  }}
                r.sadd(key, pickle.dumps(houseList_info))
        r.expire(key, 86400)

    except Exception:
        import traceback
        traceback.print_exc()


t3 = PythonOperator(
    task_id='LoadBuildingListWuhanCache',
    python_callable=query_mongodb,
    op_kwargs={'name': 'BuildingList', 'key': REDIS_BUILDING_CACHE_KEY},
    dag=dag)

builfing_info_list = list(map(lambda x: json.loads(
    x.decode()), dj_settings.REDIS_CACHE.smembers(REDIS_BUILDING_CACHE_KEY)))
t4 = PythonOperator(
    task_id='LoadBuildingListWuhan',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': builfing_info_list},
    dag=dag)
t4.set_upstream(t3)

t5 = PythonOperator(
    task_id='LoadBuildingListWuhanCache',
    python_callable=query_mongodb,
    op_kwargs={'name': 'HouseList', 'key': REDIS_HOUSE_CACHE_KEY},
    dag=dag)

builfing_info_list = list(map(lambda x: json.loads(
    x.decode()), dj_settings.REDIS_CACHE.smembers(REDIS_HOUSE_CACHE_KEY)))
t6 = PythonOperator(
    task_id='LoadHouseListWuhan',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': builfing_info_list},
    dag=dag)
t6.set_upstream(t5)
