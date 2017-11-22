# -*-coding=utf-8-*-

import sys
import json
from celery import shared_task
from celery.signals import worker_shutdown, worker_ready
if sys.version_info.major >= 3:
    import urllib.request as urllib_use
else:
    import urllib2 as urllib_use

monitor_api = 'http://192.168.14.33:9000'
src_name = 'fangtianxia'
instance_name = 'ProxyService2'


@shared_task(bind=True)
def monitor_post(self, Action, Src=src_name, Instance=instance_name, Msg=""):
    if Action in ['start', 'end', 'running', 'error']:
        data = {'Action': Action,
                    'Src': Src,
                    'Instance': Instance,
                    'Msg': Msg}
        print(data)
        urllib_use.urlopen(url=monitor_api, data=(json.dumps(data)).encode('utf-8'))
    else:
        pass


@worker_shutdown.connect
def _stop_signal(*args, **kwarg):
    monitor_post(Action='end')


@worker_ready.connect
def _start_signal(*args, **kwarg):
    monitor_post(Action='start')
