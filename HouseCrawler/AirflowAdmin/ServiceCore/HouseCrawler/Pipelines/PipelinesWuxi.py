# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import random
import uuid
import json
import redis
from HouseCrawler.Items.ItemsWuxi import *

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.njhouse.com.cn",
            'Cache-Control': "max-age=0",
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def safe_format_value(self, value):
        try:
            value = '%.05f' % float(value)
            return str(value)
        except Exception:
            pass
        if isinstance(value, dict):
            try:
                value = dict(value)
                return value
            except Exception:
                pass
        if isinstance(value, list):
            try:
                value = value.sort()
                return value
            except Exception:
                pass
        return str(value)
    def check_change(self, item, q_object):
        check_item_flag = False
        monitorkeys = {'HouseSts'}
        mainmonitorkeys = {'HouseSts','OnSoldNumber'}
        copymainmonitorkeys = {}
        nowtime = str(datetime.datetime.now())
        changedata = ''
        if q_object:
            q_object.NewCurTimeStamp = nowtime
            q_object.save()
            for key in item:
                if not hasattr(q_object, key):
                    check_item_flag = True
                    break
                if key not in mainmonitorkeys:
                    continue
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(q_object, key)):
                    changedata = changedata + 'now' + key + ':' + str(item.get(key)) + ',' \
                                 + 'last' + key + ':' + str(getattr(q_object, key)) + ';'
                    check_item_flag = True
                if check_item_flag:
                    for nowkey in item:
                        if nowkey in copymainmonitorkeys:
                            if self.safe_format_value(getattr(q_object, nowkey)).strip() != "" \
                                    and self.safe_format_value(item.get(key)).strip() == "":
                                item[nowkey] = getattr(q_object, nowkey)
            if (isinstance(item, HouseBaseItem) or isinstance(item, MonitorHouseBaseItem)) and check_item_flag:
                for key in monitorkeys:
                    if key not in mainmonitorkeys:
                        continue
                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(q_object, key)):
                        item[key + 'Latest'] = getattr(q_object, key)
            item['change_data'] = changedata

            return check_item_flag, item
        else:
            item['change_data'] = 'new'
            check_item_flag = True
            return check_item_flag, item

    def check_item(self, item):
        check_item_flag = False
        q_object = item.django_model.objects
        try:
            if isinstance(item, MonitorProjectBaseItem):
                res_object = q_object.filter(ProjectNo=item['ProjectNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug('No MonitorProjectBaseItem')

        try:
            if isinstance(item, ProjectBaseItem):
                res_object = q_object.filter(ProjectNo=item['ProjectNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug('No ProjectBaseItem')
        try:
            if isinstance(item, MonitorHouseBaseItem):
                res_object = q_object.filter(HouseNo=item['HouseNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug('No MonitorHouseBaseItem')


        try:
            if isinstance(item, DeveloperBaseItem):
                res_object = q_object.filter(DeveloperNo=item['DeveloperNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug('No DeveloperBaseItem')

        try:
            if isinstance(item, HouseBaseItem):
                res_object = q_object.filter(HouseNo=item['HouseNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)

        except:
            logging.debug('No HouseBaseItem')
        return check_item_flag, item

    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['CurTimeStamp'] = str(datetime.datetime.now())
            item.save()
            logger.debug("storage item: %(item)s",
                         {'item': item})

    def process_item(self, item, spider):
        if item:
            check_item_flag, now_item = self.check_item(item)
            if check_item_flag:
                logger.debug("item: %(item)s change or met first",
                             {'item': now_item})
                self.storage_item(now_item)
            else:
                logger.debug("item: %(item)s UUID existed",
                             {'item': now_item})





