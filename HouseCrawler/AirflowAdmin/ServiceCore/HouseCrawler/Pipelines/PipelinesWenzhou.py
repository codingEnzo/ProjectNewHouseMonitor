#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import datetime
import uuid
from HouseCrawler.Items.ItemsWenzhou import *

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self, settings):
        self.settings = settings

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

    def check_item_exist(self, item):
        exist_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            res_object = q_object.filter(ProjectNo = item['ProjectNo']).latest(field_name = 'CurTimeStamp')
            if res_object:
                exist_flag = True
        elif isinstance(item, DeveloperBaseItem):
            res_object = q_object.filter(DeveloperNo = item['DeveloperNo']).latest(field_name = 'CurTimeStamp')
            if res_object:
                exist_flag = True
        elif isinstance(item, BuildingBaseItem):
            res_object = q_object.filter(BuildingNo = item['BuildingNo']).latest(field_name = 'CurTimeStamp')
            if res_object:
                exist_flag = True
        elif isinstance(item, HouseBaseItem):
            res_object = q_object.filter(HouseNo = item['HouseNo']).latest(field_name = 'CurTimeStamp')
            if res_object:
                exist_flag = True
        else:
            pass
        return exist_flag

    def check_item_change(self, item):
        diff_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            res_object = q_object.filter(ProjectNo = item['ProjectNo']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, DeveloperBaseItem):
            res_object = q_object.filter(DeveloperNo = item['DeveloperNo']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, BuildingBaseItem):
            res_object = q_object.filter(BuildingNo = item['BuildingNo']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, HouseBaseItem):
            res_object = q_object.filter(HouseNo = item['HouseNo']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
            if diff_flag:
                item['HouseStsLatest'] = getattr(res_object, 'HouseStsLatest')
        else:
            pass
        return diff_flag, item

    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['CurTimeStamp'] = str(datetime.datetime.now())
            item.save()
            logger.debug("storage item: %(item)s",
                         {'item': item})

    def process_item(self, item, spider):
        if item:
            item_exist_flag = self.check_item_exist(item)
            if item_exist_flag:
                logger.debug("item: %(item)s UUID existed",
                             {'item': item})
                diff_result, diff_item = self.check_item_change(item)
                if diff_result:
                    self.storage_item(diff_item)
            else:
                logger.debug("item: %(item)s met first",
                             {'item': item})
                self.storage_item(item)
            return item
