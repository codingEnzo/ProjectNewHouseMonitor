# -*- coding: utf-8 -*-
import datetime
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
		'HouseCrawler.Pipelines.PipelinesGuangzhou.PipelineGuangzhou': 300,
	},
	'SPIDER_MIDDLEWARES': {
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.ProjectBaseHandleMiddleware': 103,
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.IframePageHandleMiddleware': 104,
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.PermitInfoHandleMiddleware': 104,
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.ProjectInfoHandleMiddleware': 105,
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.PresellInfoHandleMiddleware': 106,
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.BuildingListHandleMiddleware': 107,
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.SellFormInfoHandleMiddleware': 108,
		'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresGuangzhou.HouseInfoHandleMiddleware': 109,
	},
	'RETRY_ENABLE': True,
	'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
	'CONCURRENT_REQUESTS': 64,
	'DEFAULT_REQUEST_HEADERS': {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
	},
	'POST_DEFAULT_REQUEST_HEADERS': {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'Content-Type': 'application/x-www-form-urlencoded'
	},
	'DOWNLOADER_MIDDLEWARES': {
		'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
		'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware': None,
	}
}

dag = DAG('NewHouseGuangzhou', default_args=default_args, schedule_interval="30 5 * * *")

t1 = PythonOperator(
	task_id='LoadProjectBaseGuangzhou',
	python_callable=spider_call,
	op_kwargs={
		'spiderName': 'DefaultCrawler',
		'settings': spider_settings,
		'urlList': [
			{'source_url': 'http://housing.gzcc.gov.cn/fyxx/fdcxmxx/index_1.shtml',
			 'meta': {'PageType': 'ProjectBase', 'GetPage': True}}
		]
	},
	dag=dag
)

cur = ProjectInfoGuangzhou.objects.all()
buildingList_info = []
for item in cur:
	if item['ProjectID']:
		url = 'http://housing.gzcc.gov.cn/search/project/sellForm.jsp?pjID={ProjectID}&presell={PresalePermitNumber}&chnlname=ysz'
		buildingList_info = {'source_url': url.format(ProjectID=item['ProjectID'],
		                                              PresalePermitNumber=item['PresalePermitNumber']),
		                     'meta': {'PageType': 'BuildingList',
		                              'ProjectID': item['ProjectID'],
		                              'ProjectUUID': str(item['ProjectUUID']),
		                              'ProjectName': item['ProjectName'],
		                              }
		                     }
		buildingList_info.append(buildingList_info)

t2 = PythonOperator(
	task_id='LoadBuildingListGuangzhou',
	python_callable=spider_call,
	op_kwargs={'spiderName': 'DefaultCrawler',
	           'settings': spider_settings,
	           'urlList': buildingList_info},
	dag=dag)

# t2.set_upstream(t1)
