# coding = utf-8
import datetime
import logging
import os
import sys
import uuid

import django_mongoengine
from HouseCrawler.Items.ItemsYantai import *

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class PipelineYantai(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def safe_format_value(self, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        try:
            value = '%.05f' % float(value)
            return str(value)
        except Exception:
            pass
        try:
            value = eval(value)
            return value
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
            if q_object.filter(ProjectUUID = item['ProjectUUID']).latest(field_name = 'CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, ProjectInfoItem):
            if q_object.filter(ProjectUUID = item['ProjectUUID']).latest(field_name = 'CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, PresellInfoItem):
            if q_object.filter(PresellUUID = item['PresellUUID']).latest(field_name = 'CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, BuildingInfoItem):
            if q_object.filter(BuildingUUID = item['BuildingUUID']).latest(field_name = 'CurTimeStamp'):
                exist_flag = True
        elif isinstance(item, HouseInfoItem):
            if q_object.filter(HouseUUID = item['HouseUUID']).latest(field_name = 'CurTimeStamp'):
                exist_flag = True
        else:
            pass
        return exist_flag

    def check_item_change(self, item):
        diff_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            res_object = q_object.filter(ProjectUUID = item['ProjectUUID']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, ProjectInfoItem):
            res_object = q_object.filter(ProjectUUID = item['ProjectUUID']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, PresellInfoItem):
            res_object = q_object.filter(PresellUUID = item['PresellUUID']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, BuildingInfoItem):
            res_object = q_object.filter(BuildingUUID = item['BuildingUUID']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, HouseInfoItem):
            res_object = q_object.filter(HouseUUID = item['HouseUUID']).latest(field_name = 'CurTimeStamp')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
            if diff_flag:
                item['HouseStateLatest'] = getattr(res_object, 'HouseState')
        return diff_flag, item

    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['CurTimeStamp'] = str(datetime.datetime.now())
            item.save()
            logger.debug("storage item: %(item)s", {'item': item})

    def replace_str(self, item):
        for key in item:
            if key == 'CurTimeStamp':
                continue
            field = item.django_model._meta.get_field(key)
            if isinstance(field, django_mongoengine.fields.StringField):
                try:
                    if item[key]:
                        value = str(item[key])
                        item[key] = value.replace(' ', '').replace('\r', '') \
                            .replace('\t', '').replace('\n', '').strip()
                    else:
                        item[key] = ''
                except:
                    item[key] = ''

    def process_item(self, item, spider):
        if item:
            self.replace_str(item)
            if self.check_item_exist(item):
                logger.debug("item: %(item)s UUID existed", {'item': item})
                diff_result, diff_item = self.check_item_change(item)
                if diff_result:
                    logger.debug("item: %(item)s changed", {'item': item})
                    self.storage_item(item)
            else:
                logger.debug("item: %(item)s met first", {'item': item})
                self.storage_item(item)
            return item