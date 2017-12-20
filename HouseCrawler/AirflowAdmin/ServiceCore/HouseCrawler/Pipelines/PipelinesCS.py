# coding = utf-8
import sys
import os
import logging
import uuid
import datetime
from HouseCrawler.Items.ItemsCS import *
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class CSPipeline(object):

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

    def check_item(self, item):
        exist_flag = False
        blank_count = 0
        for key in item:
            if item.get(key) in (None, ''):
                blank_count += 1
        if blank_count >= 0.8 * len(item):
            exist_flag = True
        return exist_flag

    def check_item_exist(self, item):
        exist_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            if q_object.filter(ProjectRegUUID=item['ProjectRegUUID']).latest(field_name='CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, ProjectInfoItem):
            if q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, BuildingInfoItem):
            if q_object.filter(BuildingUUID=item['BuildingUUID']).latest(field_name='CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, HouseInfoItem):
            if q_object.filter(HouseUUID=item['HouseUUID']).latest(field_name='CurTimeStamp'):
                exist_flag = True
        else:
            pass
        return exist_flag

    def check_item_change(self, item):
        diff_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            res_object = q_object.filter(ProjectRegUUID=item['ProjectRegUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, ProjectInfoItem):
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, BuildingInfoItem):
            res_object = q_object.filter(BuildingUUID=item['BuildingUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, HouseInfoItem):
            res_object = q_object.filter(HouseUUID=item['HouseUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
            if diff_flag:
                for key in ('HouseSaleState', ):
                    item[key + 'Latest'] = getattr(res_object, key)
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
            if not self.check_item(item):
                if self.check_item_exist(item):
                    logger.debug("item: %(item)s UUID existed",
                                    {'item': item})
                    diff_result, diff_item = self.check_item_change(item)
                    if diff_result:
                        logger.debug("item: %(item)s changed",
                                        {'item': item})
                        self.storage_item(item)
                else:
                    logger.debug("item: %(item)s met first",
                                    {'item': item})
                    self.storage_item(item)
            return item
