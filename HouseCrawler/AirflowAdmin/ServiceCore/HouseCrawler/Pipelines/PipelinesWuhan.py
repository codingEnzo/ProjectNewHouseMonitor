# coding = utf-8
import sys
import os
import logging
import uuid
import datetime
from HouseNew.models import *
from HouseCrawler.Items.ItemsWuhan import *
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class WuhanPipeline(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def sum_value_hash(self, value):

        def sum_value_hash(value):
            if not value:
                value = ''
            try:
                value = '%.05f' % float(value)
            except Exception:
                pass
            return hash(str(value))

        if isinstance(value, dict):
            return sum([self.sum_value_hash(value.get(key)) for key in value])
        elif isinstance(value, list):
            return sum([self.sum_value_hash(item) for item in value])
        else:
            return sum([sum_value_hash(value), ])

    def check_item(self, item):
        exist_flag = False
        blank_count = 0
        for key in item:
            if item.get(key) in (None, ''):
                blank_count += 1
        if blank_count >= 0.8 * len(item):
            exist_flag = True
        return exist_flag

    def check_item_exist(self, item):  # 检查item是否存在
        exist_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(
                field_name='CurTimeStamp')
            if res_object:
                exist_flag = True
        elif isinstance(item, ProjectInfoItem):
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(
                field_name='CurTimeStamp')
            if res_object:
                exist_flag = True
        elif isinstance(item, BuildingInfoItem):
            res_object = q_object.filter(BuildingUUID=item['BuildingUUID']).latest(
                field_name='CurTimeStamp')
            if res_object:
                exist_flag = True
        elif isinstance(item, HouseInfoItem):
            res_object = q_object.filter(HouseUUID=item['HouseUUID']).latest(
                field_name='CurTimeStamp')
            if res_object:
                exist_flag = True
        else:
            pass
        return exist_flag

    def check_item_change(self, item):  # 检查item变化
        diff_flag = False
        q_object = item.django_model.objects
        if isinstance(item, HouseInfoItem):
            res_object = q_object.filter(HouseUUID=item['HouseUUID']).latest(
                field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
            if diff_flag:
                for key in ('State',):
                    item[key + 'Latest'] = getattr(res_object, key)

        elif isinstance(item, ProjectInfoItem):
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(
                field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
                    break

        elif isinstance(item, BuildingInfoItem):
            res_object = q_object.filter(BuildingUUID=item['BuildingUUID']).latest(
                field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
                    break

        elif isinstance(item, ProjectBaseItem):  # 判断item 是否是ProjectBaseItem的一个实例
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(
                field_name='CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                    diff_flag = True
                    break

        return diff_flag, item

    def storage_item(self, item):  # 存储 item
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
