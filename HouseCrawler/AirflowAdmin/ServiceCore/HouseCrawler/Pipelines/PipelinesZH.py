# coding = utf-8
import sys
import os
import logging
import uuid
import datetime
import redis
import json
import copy
from HouseCrawler.Items.Items import *
import configparser

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))


configpath = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))) + '/city.config'
config = configparser.RawConfigParser()
config.read(configpath)
city_name = config.get('city', 'name')

host_type = config.get('redis', 'host_type')
host = config.get('redis', 'host_local') if host_type == 'local' else config.get(
    'redis', 'host_service')

logger = logging.getLogger(__name__)
r = redis.Redis(host, 6379)


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

    def check_item_change(self, item):
        exist_flag = False
        q_object = item.django_model.objects

        if isinstance(item, House_Detail_Item):
            res_object = q_object.filter(
                HouseUUID=item['HouseUUID']).latest(field_name='RecordTime')
            diff_key = ["HouseSaleState", "PresaleState", 'Price']
            if res_object:
                exist_flag = 'same'
                for i in diff_key:
                    if self.safe_format_value(item.get(i)) != self.safe_format_value(getattr(res_object, i)):
                        exist_flag = 'diff'
                        record_key = i + 'Latest'
                        item[record_key] = getattr(res_object, i)
                if exist_flag != 'diff':
                    item = res_object
            return exist_flag, item
        # 珠海城市存在预售证有不同时期的url共存,估计为预售证延期（例：预售证 DMS2014012-4).
        # 避免不同时期下的户状态差异导致状态反复变化同一项目、同一预售证下只留LssueDate为最近的数据，
        # 假若LssueDate一样则检查除'SourceUrl','PageNumber',"CheackTimeLatest"外的数值是否有变化)'''
        elif isinstance(item, Project_Detail_Item):
            res_object = q_object.filter(PresalePermitNumberUUID=item[
                                         'PresalePermitNumberUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                out_cheack = ['SourceUrl', 'PageNumber', "CheackTimeLatest"]
                RecordLssueDate = res_object.LssueDate
                if item['LssueDate'] > RecordLssueDate:
                    exist_flag = 'update'
                    for i in item:
                        res_object[i] = item[i]
                elif item['LssueDate'] == RecordLssueDate:
                    for key in item:
                        if self.safe_format_value(item.get(key) != self.safe_format_value(getattr(res_object, key))) and \
                                key not in out_cheack:
                            exist_flag = 'diff'
                if exist_flag != 'diff':
                    item = res_object
            return exist_flag, item

        elif isinstance(item, Building_Detail_Item):
            res_object = q_object.filter(
                BuildingUUID=item['BuildingUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                out_cheack = ['SourceUrl', 'PageNumber',
                              "CheackTimeLatest", 'RecordTime']
                RecordLssueDate = res_object.LssueDate
                if item['LssueDate'] > RecordLssueDate:
                    exist_flag = 'update'
                    for i in item:
                        res_object[i] = item[i]
                elif item['LssueDate'] == RecordLssueDate:
                    # 拦截同一发证日期下url却不同避免反复变化
                    if item['BuildingUrl'] != res_object.BuildingUrl:
                        pass
                    else:
                        for key in item:
                            if self.safe_format_value(item.get(key) != self.safe_format_value(getattr(res_object, key))) and \
                                    key not in out_cheack:
                                exist_flag = 'diff'
                if exist_flag != 'diff':
                    item = res_object
            return exist_flag, item

        elif isinstance(item, Certificate_Detail_Item):
            res_object = q_object.filter(PresalePermitNumberUUID=item[
                                         'PresalePermitNumberUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                out_cheack = ['SourceUrl', 'PageNumber',
                              "CheackTimeLatest", 'BuiltFloorCount']
                RecordLssueDate = res_object.LssueDate
                if item['LssueDate'] > RecordLssueDate:
                    exist_flag = 'update'
                    for i in item:
                        res_object[i] = item[i]
                elif item['LssueDate'] == RecordLssueDate:
                    for key in item:
                        if self.safe_format_value(item.get(key) != self.safe_format_value(getattr(res_object, key))) and \
                                key not in out_cheack:
                            exist_flag = 'diff'
                if exist_flag != 'diff':
                    item = res_object
            return exist_flag, item
        elif isinstance(item, Monitor_Item):
            res_object = q_object.filter(
                日期=item['日期']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'update'
                if self.safe_format_value(item.get('合计套数')) != self.safe_format_value(getattr(res_object, '合计套数')):
                    for i in item:
                        res_object[i] = item[i]
                item = res_object
            return exist_flag, item

    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['RecordTime'] = str(datetime.datetime.now())
            item['CheackTimeLatest'] = str(datetime.datetime.now())
            item.save()

    def process_item(self, item, spider):

        if item:
            status, cheack_item = self.check_item_change(item)
            if status == 'same':
                # 跟踪爬取时间
                # cheack_item.CheackTimeLatest = str(datetime.datetime.now())
                # cheack_item.save()
                logger.debug("item: %(item)s cheack over",
                             {'item': cheack_item})

            elif status == 'update':
                cheack_item.CheackTimeLatest = str(datetime.datetime.now())
                cheack_item.save()

            elif status == 'diff':
                self.storage_item(cheack_item)
                logger.debug("item: %(item)s changed", {'item': cheack_item})

            elif status == False:
                self.storage_item(cheack_item)
                logger.debug("item: %(item)s  meet first",
                             {'item': cheack_item})
