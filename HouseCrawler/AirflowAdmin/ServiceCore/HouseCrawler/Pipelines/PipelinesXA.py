# coding = utf-8
import datetime
import logging
import os
import sys
import uuid

from HouseCrawler.Items.ItemsXA import *

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class XAPipeline(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def sum_value_hash(self, value):

        def safe_format_value(val):
            if not val:
                val = ''
            try:
                val = '%.05f' % float(val)
            except Exception as e:
                print(e)
            return hash(str(val))

        if isinstance(value, dict):
            return sum([self.sum_value_hash(value.get(key)) for key in value])
        elif isinstance(value, list):
            return sum([self.sum_value_hash(item) for item in value])
        else:
            return sum([safe_format_value(value), ])

    @staticmethod
    def check_item_exist(item):
        exist_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            if q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, ProjectInfoItem):
            if q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='CurTimeStamp'):
                exist_flag = True
            print(q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='CurTimeStamp'))
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
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, ProjectInfoItem):
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, BuildingInfoItem):
            res_object = q_object.filter(BuildingUUID=item['BuildingUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
                    break

        elif isinstance(item, HouseInfoItem):
            res_object = q_object.filter(HouseUUID=item['HouseUUID']).latest(field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
                    break
            if diff_flag:
                item['HouseSaleStateLatest'] = getattr(res_object, 'HouseSaleStatus')
        return diff_flag, item

    @staticmethod
    def storage_item(item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['CurTimeStamp'] = str(datetime.datetime.now())
            item.save()
            logger.debug("storage item: %(item)s",
                         {'item': item})

    def process_item(self, item, spider):
        if item:
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
