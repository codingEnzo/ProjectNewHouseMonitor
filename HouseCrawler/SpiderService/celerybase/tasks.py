# -*-coding=utf-8-*-
from __future__ import absolute_import

import os
import sys

from celery import Celery
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


sys.path.append(BASE_DIR)
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

env = 'masterLocal'

schedule_tab = {"getBindIpBeat":
                    {"task": "task_service.getBindIpBeat",
                        "schedule": 1200.0,
                        "args": (),
                        "options": {}},
                "running_beat":
                    {"task": "monitor_service.monitor_post",
                        "schedule": crontab(minute="*/5"),
                        "args": ('running',),
                        "options": {}}}

if env == 'masterLocal':
    schedule_tab = {"getProxyBeat":
                        {"task": "task_service.getProxyBeat",
                            "schedule": 15.0,
                            "args": (),
                            "options": {}},
                    "bindIpBeat":
                        {"task": "task_service.bindIpBeat",
                            "schedule": 1200.0,
                            "args": (),
                            "options": {}},
                    "getBindIpBeat":
                        {"task": "task_service.getBindIpBeat",
                            "schedule": 1200.0,
                            "args": (),
                            "options": {}},
                    "mergeIpLBeat":
                        {"task": "task_service.mergeProxyLow",
                            "schedule": 10.0,
                            "args": (),
                            "options": {}},
                    "mergeIpMBeat":
                        {"task": "task_service.mergeProxyMiddle",
                            "schedule": 10.0,
                            "args": (),
                            "options": {}},
                    "mergeIpHBeat":
                        {"task": "task_service.mergeProxyHigh",
                            "schedule": 10.0,
                            "args": (),
                            "options": {}},
                    "mergeIpLBeat2":
                        {"task": "task_service.mergeProxyLow2",
                            "schedule": 10.0,
                            "args": (),
                            "options": {}},
                    "mergeIpHBeat2":
                        {"task": "task_service.mergeProxyHigh2",
                            "schedule": 10.0,
                            "args": (),
                            "options": {}},
                    "resetIpListBeat":
                        {"task": "task_service.resetProxyList",
                            "schedule": 3600.0 * 24,
                            "args": (),
                            "options": {}},
                    "running_beat":
                        {"task": "monitor_service.monitor_post",
                            "schedule": crontab(minute="*/5"),
                            "args": ('running',),
                            "options": {}}}

app = Celery('ProxyReqService')
app.config_from_object('celeryconf')
app.conf.update(BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 2400000},
                CELERYBEAT_SCHEDULE=schedule_tab)
app.autodiscover_tasks()
