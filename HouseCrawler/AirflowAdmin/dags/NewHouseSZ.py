# -*-coding=utf-8-*-
import os
import sys
import redis
import random
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
        'HouseCrawler.Pipelines.PipelinesSZ.SZPipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSZ.GetYszBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSZ.GetProjectBaseHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSZ.GetProjectPageBaseHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSZ.BuildingHandleMiddleware': 105,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSZ.HouseHandleMiddleware': 106,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSZ.HouseInfoHandleMiddleware': 107,
    },
    'RETRY_ENABLE': True,
    'PROXY_ENABLE': False,
    'REDIRECT_ENABLED': True,
    'REDIS_HOST': '10.30.1.18',
    'REDIS_PORT': 6379,
    'CLOSESPIDER_TIMEOUT': 3600 * 5.8
}

addrs = ['工业园区', '吴中区', '相城区', '高新区', '姑苏区', '吴江区']

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Host': 'www.szfcweb.com',
    'Content-Type': 'application/x-www-form-urlencoded',
}

dag = DAG('NewHouseSZ', default_args=default_args,
          schedule_interval="15 */6 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseSZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://spf.szfcweb.com/szfcweb/DataSerach/SaleInfoProListIndex.aspx',
                            'meta': {'PageType': 'GetProjectBase', 'addr': addr}} for addr in addrs]},
    dag=dag)

t2 = PythonOperator(
    task_id='LoadProjectYszSZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://spf.szfcweb.com/szfcweb/DataSerach/MITShowList.aspx',
                            'meta': {'PageType': 'GetYszBase', 'addr': addr}} for addr in addrs]},
    dag=dag)

builfing_info_list = []
d1 = datetime.datetime.now()
cur = BuildingBaseSuzhou.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                             {'$group':
                                              {'_id': "$building_no",
                                               'CurTimeStamp': {'$last': '$CurTimeStamp'},
                                               'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                               'project_name': {'$last': '$project_name'},
                                               'building_name': {'$last': '$building_name'},
                                               'project_no': {'$last': '$project_no'},
                                               'building_no': {'$last': '$building_no'},
                                               }
                                              },
                                             ], allowDiskUse=True)
r = redis.Redis(host='10.30.1.18', port=6379)
for item in cur:
    try:
        if (item['NewCurTimeStamp'] > str(d1 - datetime.timedelta(days=1))):
            getkey = str(r.get('SuzhouCrawlerkey%d' % random.randint(0, 9))).replace(
                "b'", "").replace("'", "")
            nexturl = 'http://spf.szfcweb.com/szfcweb/%s/DataSerach/SaleInfoHouseShow.aspx?PBTAB_ID=%s&SPJ_ID=%s' \
                % (getkey, item['building_no'], item['project_no'])
            builfing_info = {'source_url': nexturl,
                             'headers': headers,
                             'meta': {'PageType': 'HouseBase',
                                      'BuildingName': item['building_name'],
                                      'project_name': item['project_name'],
                                      'retrytimes': 0
                                      }}
            builfing_info_list.append(builfing_info)
    except Exception:
        import traceback
        traceback.print_exc()
t3 = PythonOperator(
    task_id='LoadBuildingInfoSZ',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': builfing_info_list},
    dag=dag)
