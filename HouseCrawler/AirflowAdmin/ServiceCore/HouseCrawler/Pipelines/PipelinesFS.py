# coding = utf-8
import configparser
import datetime
import logging
import os
import sys
import uuid

from HouseCrawler.Items.ItemsFS import *

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class FSPipeline(object):
    def __init__(self, settings):
        self.settings = settings
        self.check_key = ['HouseUseType', 'HouseNature',
                          'HouseType',
                          'BalconyType',
                          'ForecastBuildingArea',
                          'ForecastInsideOfBuildingArea',
                          'ForecastPublicArea',
                          'MeasuredBuildingArea',
                          'MeasuredInsideOfBuildingArea',
                          'MeasuredSharedPublicArea',
                          'IsMortgage',
                          'IsAttachment',
                          'Adress',
                          'TotalPrice',
                          'ComplateTag',
                          'HouseSaleState']

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
                value.sort()
                return value
            except Exception:
                pass
        return str(value)

    def check_item_change(self, item):
        diff_flag = False
        q_object = item.django_model.objects
        if isinstance(item, House_Detail_Item):
            res_object = q_object.filter(HouseUUID=item['HouseUUID']).latest(field_name='RecordTime')
            res_tag = res_object.ComplateTag
            diff_keys = ['HouseSaleState', ]
            if not int(item['ComplateTag']):
                if self.safe_format_value(item.get('HouseSaleState')) != self.safe_format_value(
                        getattr(res_object, 'HouseSaleState')):
                    diff_flag = True
            else:
                diff_keys.extend(self.check_key)
                for key in diff_keys:
                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                        diff_flag = True
                        break
            if diff_flag:
                item['HouseSaleStateLatest'] = getattr(res_object, 'HouseSaleState')
                if (not int(item['ComplateTag'])) and int(res_tag):
                    for ck in self.check_key:
                        item[ck] = getattr(res_object, ck)
        elif isinstance(item, Project_Detail_Item):
            diff_keys = ['SourceUrl', 'Pages_num', "Pk", 'CheackTimeLatest', 'RecordTime']
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='RecordTime')
            for key in item:
                if (self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key))) and (
                            key not in diff_keys):
                    diff_flag = True
                    break
        elif isinstance(item, Building_Detail_Item):
            diff_keys = ['SourceUrl', 'PresalePermitUrl', 'CheackTimeLatest', 'RecordTime']
            res_object = q_object.filter(BuildingUUID=item['BuildingUUID']).latest(field_name='RecordTime')
            for key in item:
                if (self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key))) and (
                            key not in diff_keys):
                    diff_flag = True
        elif isinstance(item, Certificate_Detail_Item):
            diff_keys = ['SourceUrl', 'PresalePermitUrl', 'CheackTimeLatest', 'RecordTime']
            res_object = q_object.filter(PresalePermitNumberUUID=item['PresalePermitNumberUUID']).latest(
                field_name='RecordTime')
            for key in item:
                if (self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key))) and (
                            key not in diff_keys):
                    diff_flag = True
        elif isinstance(item, Monitor_Item):
            res_object = q_object.filter(riqi=item['riqi']).latest(field_name='RecordTime')
            if self.safe_format_value(item.get('quanshi_zhuzhai_taoshu')) != self.safe_format_value(
                    getattr(res_object, 'quanshi_zhuzhai_taoshu')):
                diff_flag = True

        return diff_flag, item

    @staticmethod
    def check_item_exist(item):
        exist_flag = False
        q_object = item.django_model.objects
        if isinstance(item, House_Detail_Item):
            if q_object.filter(HouseUUID=item['HouseUUID']).latest(field_name='RecordTime'):
                exist_flag = True
        elif isinstance(item, Project_Detail_Item):
            if q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='RecordTime'):
                exist_flag = True
        elif isinstance(item, Building_Detail_Item):
            if q_object.filter(BuildingUUID=item['BuildingUUID']).latest(field_name='RecordTime'):
                exist_flag = True
        elif isinstance(item, Certificate_Detail_Item):
            if q_object.filter(PresalePermitNumberUUID=item['PresalePermitNumberUUID']).latest(
                    field_name='RecordTime'):
                exist_flag = True
        elif isinstance(item, Monitor_Item):
            if q_object.filter(riqi=item['riqi']).latest(field_name='RecordTime'):
                exist_flag = True
        return exist_flag

    @staticmethod
    def storage_item(item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['RecordTime'] = str(datetime.datetime.now())
            item.save()

    def process_item(self, item, spider):
        if item:
            if self.check_item_exist(item):
                logger.debug("item: %(item)s UUID existed",
                             {'item': item})
                diff_result, diff_item = self.check_item_exist(item)
                if diff_result:
                    logger.debug("item: %(item)s changed",
                                 {'item': item})
                    if not isinstance(item, Monitor_Item):
                        self.storage_item(item)
                    else:
                        item.save()
            else:
                self.storage_item(item)
                logger.debug("item: %(item)s met first",
                             {'item': item})
