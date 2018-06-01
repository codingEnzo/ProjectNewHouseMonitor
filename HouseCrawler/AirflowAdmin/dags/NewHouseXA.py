# -*-coding=utf-8-*-
import datetime
import os
import sys

import django
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

import pickle

STARTDATE = datetime.datetime.now() - datetime.timedelta(hours=6)
REDIS_CACHE_KEY = "NewHouseXA"

default_args = {
    'owner': 'airflow',
    'start_date': STARTDATE,
    'email': ['coder.gsy@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1),
}

spider_settings = {
    'ITEM_PIPELINES': {
        'HouseCrawler.Pipelines.PipelinesXA.XAPipeline': 300,
        'HouseCrawler.Pipelines.PipelinesUtils.PipelinesCheck.CheckPipeline': 299,
    },
    'SPIDER_MIDDLEWARES': {
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.ProjectBaseHandleMiddleware': 102,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.ProjectInfoHandleMiddleware': 103,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.PresaleLicenceHandleMiddleware': 104,
        'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresXA.HouseInfoHandleMiddleware': 105,
    },
    'CLOSESPIDER_TIMEOUT': 3600 * 3.5,
    'RETRY_HTTP_CODES': [500, 403, 404, 501, 502, 503, 504, 400, 408, 411, 413, 302, 301, 407, 303, 304, 305, 306, 307],
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Host': 'www.fang99.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    },
    'USER_AGENTS': [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    ],
    'CONCURRENT_REQUESTS': 32,
    'DOWNLOAD_TIMEOUT': 60,
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware': None,
    },
    'CITY': '西安'

}

dag = DAG('NewHouseXA', default_args=default_args,
          schedule_interval="15 */4 * * *")

cache_dag = DAG('NewHouseXACache', default_args=default_args,
                schedule_interval="45 23 * * *")

t1 = PythonOperator(
    task_id='LoadProjectBaseXA',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': [{'source_url': 'http://www.fang99.com/buycenter/buildingsearch.aspx?page=1',
                            'meta': {'PageType': 'ProjectInitial'}}]},
    dag=dag
)


def query_mongodb(obj=None, name="ProjectBase", key=REDIS_CACHE_KEY):
    r = dj_settings.REDIS_CACHE
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.fang99.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    try:
        if name == "ProjectInfo" or name == 'PresaleInfo':
            cur = obj.objects.all()
            if name == "ProjectInfo":
                for item in cur:
                    project_info = {
                        'source_url': item.ProjectBaseSubURL,
                        'meta': {
                            'PageType': 'ProjectSubBase',
                            'ProjectUUID': item.ProjectUUID,
                            'ProjectName': item.ProjectName,
                            'ProjectCompany': item.ProjectCompany,
                        },
                        'headers': headers
                    }
                    r.sadd(key, pickle.dumps(project_info))
            else:
                headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                for item in cur:
                    headers['Referee'] = item.ProjectInfoURL
                    presale_info = {
                        'source_url': item.ProjectPresaleURL,
                        'meta': {
                            'PageType': 'PresaleLicenceInfo',
                            'ProjectUUID': item.ProjectUUID,
                            'ProjectName': item.ProjectName,
                        },
                        'headers': headers
                    }
                    r.sadd(key, pickle.dumps(presale_info))

        elif name == 'BuildingInfo':
            cur = obj.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
                                          {'$group': {
                                              '_id': "$BuildingUUID",
                                              'ProjectName': {'$first': '$ProjectName'},
                                              'ProjectUUID': {'$first': '$ProjectUUID'},
                                              'BuildingName': {'$first': '$BuildingName'},
                                              'BuildingUUID': {'$first': '$BuildingUUID'},
                                              'BuildingURL': {'$first': '$BuildingURL'},
                                          }}])
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'b.fang99.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
                'X-Requested-With': 'XMLHttpRequest'
            }
            for item in cur:
                if item['BuildingURL']:
                    building_info = {'source_url': item['BuildingURL'],
                                     'headers': headers,
                                     'meta': {'PageType': 'HouseInfo',
                                              'ProjectName': item['ProjectName'],
                                              'BuildingName': item['BuildingName'],
                                              'ProjectUUID': str(item['ProjectUUID']),
                                              'BuildingUUID': str(item['BuildingUUID'])}}
                    r.sadd(key, pickle.dumps(building_info))

        r.expire(key, 86400)

    except Exception:
        import traceback
        traceback.print_exc()


PROJECT_BASE_KEY = REDIS_CACHE_KEY + ':ProjectInfo'

t2 = PythonOperator(
    task_id='LoadProjectInfoCacheXA',
    python_callable=query_mongodb,
    op_kwargs={'key': PROJECT_BASE_KEY, 'obj': ProjectBaseXian, 'name': 'ProjectInfo'},
    dag=cache_dag
)

project_info_generator = map(lambda x: pickle.loads(x), dj_settings.REDIS_CACHE.smembers(PROJECT_BASE_KEY))

t3 = PythonOperator(
    task_id='LoadProjectInfoXA',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': project_info_generator},
    dag=dag)

PRESALE_INFO_KEY = REDIS_CACHE_KEY + ':PresaleInfo'

t4 = PythonOperator(
    task_id='LoadPresaleInfoCacheXA',
    python_callable=query_mongodb,
    op_kwargs={'key': PRESALE_INFO_KEY, 'obj': ProjectInfoXian, 'name': 'PresaleInfo'},
    dag=cache_dag
)

presale_info_generator = map(lambda x: pickle.loads(x), dj_settings.REDIS_CACHE.smembers(PRESALE_INFO_KEY))

t5 = PythonOperator(
    task_id='LoadPresaleInfoXA',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': presale_info_generator},
    dag=dag)

BUILDING_INFO_KEY = REDIS_CACHE_KEY + ':BuildingInfo'

t6 = PythonOperator(
    task_id='LoadBuildingInfoCacheXA',
    python_callable=query_mongodb,
    op_kwargs={'key': BUILDING_INFO_KEY, 'obj': BuildingInfoXian, 'name': 'BuildingInfo'},
    dag=cache_dag
)

building_info_generator = map(lambda x: pickle.loads(x), dj_settings.REDIS_CACHE.smembers(BUILDING_INFO_KEY))

t7 = PythonOperator(
    task_id='LoadBuildingInfoXA',
    python_callable=spider_call,
    op_kwargs={'spiderName': 'DefaultCrawler',
               'settings': spider_settings,
               'urlList': building_info_generator},
    dag=dag)
