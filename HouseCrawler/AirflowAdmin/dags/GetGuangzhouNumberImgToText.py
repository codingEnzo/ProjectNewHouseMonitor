# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import regex
from redis import Redis

import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

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

dag = DAG('GetGuangzhouNumberImgToText', default_args=default_args, schedule_interval="30 * * * *")


def getNumberImgToText():
	# 获取数字对应的图片 set
	ysz_arr = ['20170435', '20170689']
	NUMBER_IMG = {}
	for ysz in ysz_arr:
		data = {
			'projectName': '', 'presellNo': ysz,
			'developer': '', 'projectAddress': '', 'chnlname': '(unable to decode value)',
			'imgvalue': '8410', 'fdcxmxxrandinput': 'b18e8fb514012229891cf024b6436526',
			'orderfield': '', 'ordertype': '', 'Submit': '(unable to decode value)',
			'currPage': '0', 'judge': ''
		}
		url = 'http://www.gzcc.gov.cn/housing/search/project/projectSearch.jsp'
		response = requests.post(url, data)
		soup = BeautifulSoup(response.text, 'html.parser')
		elements = soup.select('table#tab > tr:nth-of-type(1) > td:nth-of-type(4) > a > img ')
		for i, element in enumerate(elements):
			t = regex.search(r'/images/(.+)\.gif', str(element['src']))
			if t:
				key = t.group(1)
				NUMBER_IMG[key] = ysz[i]
	if len(NUMBER_IMG) == 10:
		r = Redis(host='120.25.213.19', port=6379, db=1, decode_responses=True)
		r.set('NUMBER_IMG', NUMBER_IMG)


t1 = PythonOperator(
	task_id='GetGuangzhouNumberImgToText_task',
	python_callable=getNumberImgToText,
	dag=dag
)
