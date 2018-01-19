# coding = utf-8
import configparser
import datetime
import logging
import os
import sys
import uuid

from HouseCrawler.Items.ItemsHuizhou import *

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class PipelineHuizhou(object):
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



    def check_item_exist(self,item):
        exist_flag = False
        q_object = item.django_model.objects
        if isinstance(item, House_Detail_Item):
            if q_object.filter(HouseUUID = item['HouseUUID']).latest(field_name = 'RecordTime'):
                exist_flag = True
        if isinstance(item, Project_Detail_Item):
            if q_object.filter(ProjectUUID = item['ProjectUUID']).latest(field_name = 'RecordTime'):
                exist_flag = True
        elif isinstance(item, Building_Detail_Item):
            if q_object.filter(BuildingUUID = item['BuildingUUID']).latest(field_name = 'RecordTime'):
                exist_flag = True
        elif isinstance(item, Certificate_Detail_Item):
            if q_object.filter(PresalePermitNumberUUID = item['PresalePermitNumberUUID']).latest(field_name = 'RecordTime'):
                exist_flag = True
        elif isinstance(item, Monitor_Item):
            if q_object.filter(riqi = item['riqi']).latest(field_name = 'RecordTime'):
                exist_flag = True
        else:
            pass
        return exist_flag

    def check_item_change(self,item):
        diff_flag = False
        q_object = item.django_model.objects
        if isinstance(item, Project_Detail_Item):
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='RecordTime')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, Building_Detail_Item):
            res_object = q_object.filter(BuildingUUID = item['BuildingUUID']).latest(field_name = 'RecordTime')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, Certificate_Detail_Item):
            res_object = q_object.filter(PresalePermitNumberUUID = item['PresalePermitNumberUUID']).latest(field_name = 'RecordTime')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        elif isinstance(item, House_Detail_Item):
            res_object = q_object.filter(HouseUUID = item['HouseUUID']).latest(field_name = 'RecordTime')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
            if diff_flag:
                item['HouseSaleStateLatest'] = getattr(res_object, 'HouseSaleState')
        elif isinstance(item, Monitor_Item):
            res_object = q_object.filter(riqi = item['riqi']).latest(field_name = 'RecordTime')
            for key in item:
                if not hasattr(res_object, key):
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    diff_flag = True
                    break
        else:
            pass
        return diff_flag,item
    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['RecordTime'] = str(datetime.datetime.now())
            item.save()

    def process_item(self, item, spider):
        if item:
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