# -*- coding: utf-8 -*-
import datetime
import os
import sys

import django
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

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
        'HouseCrawler.Pipelines.PipelinesCangzhou.Pipeline': 300,
    },
    'SPIDER_MIDDLEWARES': {
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerProject': 101,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerLand': 102,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerPlanning': 103,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerConstruction': 104,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerConstructionLandPlanning': 105,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerDeveloper': 106,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerPresale': 107,
        # 'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresCangzhou.SpiderMiddlerHouse': 108,
    },
    'RETRY_ENABLE': True,
    'CLOSESPIDER_TIMEOUT': 3600 * 7.5,
    'CONCURRENT_REQUESTS': 64,
    'USER_AGENTS':[
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    ]
}

dag = DAG('NewHouseCangzhou', default_args=default_args, schedule_interval="30 */8 * * *")

headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.hbczfdc.com:4993",
            'Cache-Control': "max-age=0",
}

t1 = PythonOperator(
    task_id='LoadProjectBaseCangzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [
            {'source_url': 'http://www.hbczfdc.com:4993/hpms/ProjectInfoList.aspx',
             'headers': headers,
             'meta': {'PageType': 'ProjectBase', 'pagenum': 1}}
        ]
    },
    dag=dag
)

t2 = PythonOperator(
    task_id='LoadDeveloperBaseCangzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': [
            {'source_url': 'http://www.hbczfdc.com:4993/HEMS/CompanyList.aspx?type=1',
             'headers': headers,
             'meta': {'PageType': 'DeveloperBase', 'pagenum': 1}}
        ]
    },
    dag=dag
)


cur = ProjectBaseCangzhou.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                             {'$group':
                                                 {'_id': "$ProjectNo",
                                                  'CurTimeStamp':{'$last': '$CurTimeStamp'},
                                                  'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                                  'change_data': {'$last': '$change_data'},
                                                  'presellInfoCode':{'$last': '$presellInfoCode'},
                                                  'buildInfoCode': {'$last': '$buildInfoCode'},
                                                  'tdzInfoCode': {'$last': '$tdzInfoCode'},
                                                  'sgxkzInfoCode': {'$last': '$sgxkzInfoCode'},
                                                  'jsydghxkzInfoCode': {'$last': '$jsydghxkzInfoCode'},
                                                  'ghxkzInfo': {'$last': '$ghxkzInfo'},
                                                  'ProjectName': {'$last': '$ProjectName'},
                                                  'ProjectNo': {'$last': '$ProjectNo'},
                                                  'ProjectCode': {'$last': '$ProjectCode'},

                                                 }
                                             }])
req_list = []

for item in cur:
    buildInfoCode = item['buildInfoCode']
    ProjectName = item['ProjectName']
    ProjectNo = item['ProjectNo']
    ProjectCode = item['ProjectCode']
    change_data = item['change_data']
    presellInfoCode = item['presellInfoCode']
    buildInfoCode = item['buildInfoCode']
    tdzInfoCode = item['tdzInfoCode']
    sgxkzInfoCode = item['sgxkzInfoCode']
    jsydghxkzInfoCode = item['jsydghxkzInfoCode']
    ghxkzInfo = item['ghxkzInfo']

    if buildInfoCode:
        for buildInfo in buildInfoCode.split(";;"):
            buildCode = buildInfo.split(',,')
            InfoUrl = 'http://www.hbczfdc.com:4993/Common/Agents/ExeFunCommon.aspx'
            body = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\
                                      <param funname="SouthDigital.Wsba2.CBuildTableV2.GetBuildHTMLEx">\
                                      <item>../</item>\
                                      <item>%s</item>\
                                      <item>1</item>\
                                      <item>1</item>\
                                      <item>80</item>\
                                      <item>840</item>\
                                      <item>g_oBuildTable</item>\
                                      <item> 1=1</item>\
                                      <item>1</item>\
                                      <item></item>\
                                      <item></item>\
                                      </param>' % (buildCode[0])
            req_body = urlparse.quote(body)
            house_base = {
                'source_url': InfoUrl,
                'headers': headers,
                'body': req_body,
                'method': 'POST',
                'meta': {
                    'PageType': 'HouseBase',
                    'ProjectName': ProjectName,
                    'ProjectNo': ProjectNo,
                    'BuildName': buildCode[1],
                    'ProjectCode': ProjectCode,
                    'BuildCode': buildCode[0]
                }}
            req_list.append(house_base)

    if presellInfoCode:
        for presellInfo in presellInfoCode.split(";;"):
            presellCode = presellInfo.split(',,')
            InfoUrl = 'http://www.hbczfdc.com:4993/HPMS/presellCertInfo.aspx?code=' + presellCode[0]
            presell_base = {
                'source_url': InfoUrl,
                'headers': headers,
                'method': 'GET',
                'meta': {'PageType': 'PresaleBase',
                         'ProjectName': ProjectName,
                         'ProjectNo': ProjectNo,
                         }}
            req_list.append(presell_base)

    if tdzInfoCode:
        for tdzInfo in tdzInfoCode.split(";;"):
            tdzCode = tdzInfo.split(',,')
            InfoUrl = 'http://www.hbczfdc.com:4993/HPMS/tdzInfo.aspx?code=%s' % \
                      tdzCode[0]

            land_base = {
                'source_url': InfoUrl,
                'headers': headers,
                'method': 'GET',
                'meta': {'PageType': 'LandBase',
                         'ProjectName': ProjectName,
                         'ProjectNo': ProjectNo,
                         }}
            req_list.append(land_base)
    if sgxkzInfoCode:
        for sgxkzInfo in sgxkzInfoCode.split(";;"):
            sgxkzCode = sgxkzInfo.split(',,')
            InfoUrl = 'http://www.hbczfdc.com:4993/HPMS/sgxkzInfo.aspx?code=%s' % \
                      sgxkzCode[0]

            construction_base = {
                'source_url': InfoUrl,
                'headers': headers,
                'method': 'GET',
                'meta': {'PageType': 'ConstructionBase',
                         'ProjectName': ProjectName,
                         'ProjectNo': ProjectNo,
                         }}
            req_list.append(construction_base)
    if ghxkzInfo:
        for ghxkz in ghxkzInfo.split(";;"):
            sgxkz = ghxkz.split(',,')
            InfoUrl = 'http://www.hbczfdc.com:4993/HPMS/jsgcghxkzInfo.aspx?code=%s' % sgxkz[0]

            planningBase = {'source_url': InfoUrl,
                            'headers': headers,
                            'method': 'GET',
                            'meta':
                                {'PageType': 'PlanningBase',
                                 'ProjectName': ProjectName,
                                 'ProjectNo': ProjectNo,
                                 }}
            req_list.append(planningBase)
    if jsydghxkzInfoCode:
        for jsydghxkzInfo in jsydghxkzInfoCode.split(";;"):
            jsydghxkzInfo = jsydghxkzInfo.split(',,')
            InfoUrl = 'http://www.hbczfdc.com:4993/HPMS/jsydghxkzInfo.aspx?code=%s' % jsydghxkzInfo[0]

            constructionLandPlanningBase = {'source_url': InfoUrl,
                            'headers': headers,
                            'method': 'GET',
                            'meta':
                                {'PageType': 'ConstructionLandPlanningBase',
                                 'ProjectName': ProjectName,
                                 'ProjectNo': ProjectNo,
                                 }}

            req_list.append(constructionLandPlanningBase)



t3 = PythonOperator(
    task_id='LoadInfoCangzhou',
    python_callable=spider_call,
    op_kwargs={
        'spiderName': 'DefaultCrawler',
        'settings': spider_settings,
        'urlList': req_list
    },
    dag=dag
)
