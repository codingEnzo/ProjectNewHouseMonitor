# coding = utf-8
import sys
import os
import logging
import uuid

import datetime

import django_mongoengine
from scrapy.exceptions import DropItem
from HouseCrawler.Items.ItemsTianjin import *
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class PipelineTianjin(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def sum_value_hash(self, value):

        def safe_format_value(value):
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
            return sum([safe_format_value(value), ])

    def check_item_change(self, item):
        no_monit_key = ('SourceUrl', 'UnitID', 'BuildingID',
                        'ProjectUrl', 'RecordTime', 'CheackTimeLatest')
        exist_flag = False
        q_object = item.django_model.objects
        if isinstance(item, House_Detail_Item):
            res_object = q_object.filter(
                HouseUUID=item['HouseUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                for key in item:
                    if key in no_monit_key:
                        continue
                    if not hasattr(res_object, key):
                        exist_flag = 'diff'
                        break
                    if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                        exist_flag = 'diff'
                        break
            if exist_flag == 'diff':
                item['HouseSaleStateLatest'] = getattr(
                    res_object, 'HouseSaleState')
        elif isinstance(item, Project_Detail_Item):
            res_object = q_object.filter(
                ProjectUUID=item['ProjectUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                for key in item:
                    if key in no_monit_key:
                        continue
                    if not hasattr(res_object, key):
                        exist_flag = 'diff'
                        break
                    if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                        exist_flag = 'diff'
                        break
        elif isinstance(item, Building_Detail_Item):
            res_object = q_object.filter(
                BuildingUUID=item['BuildingUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                for key in item:
                    if key in no_monit_key:
                        continue
                    if not hasattr(res_object, key):
                        exist_flag = 'diff'
                        break
                    if self.sum_value_hash(item.get(key)) != self.sum_value_hash(getattr(res_object, key)):
                        exist_flag = 'diff'
                        break
        else:
            pass
        return exist_flag, item

    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['RecordTime'] = str(datetime.datetime.now())
            item.save()

    def replace_str(self, item):
        for key in item:
            if key in ('CheackTimeLatest', 'RecordTime'):
                continue
            field = item.django_model._meta.get_field(key)
            if isinstance(field, django_mongoengine.fields.StringField):
                try:
                    if item[key]:
                        value = str(item[key])
                        item[key] = value.replace(' ', '').replace('\r', '') \
                            .replace('\t', '').replace('\n', '').replace('　', '').strip()
                    else:
                        item[key] = ''
                except:
                    item[key] = ''

    def process_item(self, item, spider):
        if item:
            self.replace_str(item)
            status, cheack_item = self.check_item_change(item)
            if status:
                if status == 'diff':
                    self.storage_item(cheack_item)
                else:
                    raise DropItem('Drop no change item')
            else:
                self.storage_item(cheack_item)
        return item
