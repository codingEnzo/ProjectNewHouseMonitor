# coding = utf-8
import configparser
import datetime
import logging
import os
import sys
import uuid

from HouseCrawler.Items.ItemsHuizhou import *
from scrapy.http import Request

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class PipelineHuizhou(object):
    def __init__(self, settings, spider):
        self.settings = settings
        self.spider = spider

        self.record_key1 = ['HouseUseType', 'HouseUse', 'UnitShape',
                            'FloorName', 'FloorHight', 'Toward',
                            'BuildingStructure', 'IsPublicMating',
                            'IsMoveBack', 'IsPrivateUse', 'IsPermitSale',
                            'Balconys', 'UnenclosedBalconys', 'Kitchens',
                            'Toilets', 'SalePriceList', 'ForecastPublicArea',
                            'ForecastInsideOfBuildingArea', 'ForecastBuildingArea',
                            'MeasuredBuildingArea', 'MeasuredInsideOfBuildingArea',
                            'MeasuredSharedPublicArea', 'IsMortgage', 'IsAttachment', 'ComplateTag',
                            'Address',
                            ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler.spider)

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

    # 调用spider的request
    def make_request(self, req):
        self.spider.crawler.engine.crawl(request=req, spider=self.spider)

    def check_item_change(self, item):

        exist_flag = False

        q_object = item.django_model.objects

        # ComplateTag表示完整性，1表示完整，0表示不完整
        if isinstance(item, House_Detail_Item):
            res_object = q_object.filter(HouseUUID=item['HouseUUID']).latest(field_name='RecordTime')
            diff_key1 = ["HouseSaleState"]
            update_key = []
            if res_object:
                exist_flag = 'same'
                tag_flag = res_object.ComplateTag
                for i in diff_key1:
                    if self.safe_format_value(item.get(i)) != self.safe_format_value(getattr(res_object, i)):
                        exist_flag = 'diff'
                        oldrecord = i + 'Latest'
                        item[oldrecord] = getattr(res_object, i)
                        # 根据complatetag值和res_object来判断是否进行请求,当发现数据集库不存在，以及complatetag为0发出请求
            elif not int(item['ComplateTag']):
                # 携带该不完整的item发出请求，同时抛弃该item
                exist_flag = 'drop'
                req = Request(url=item['HouseUrl'], method='GET', meta={'PageType': 'hd_url2', "Item": item},
                              dont_filter=True)
                self.make_request(req)
            if exist_flag == 'diff':
                for i in self.record_key1:
                    item[i] = getattr(res_object, i)
            elif exist_flag == 'same':
                item = res_object
            return exist_flag, item

        elif isinstance(item, Project_Detail_Item):
            res_object = q_object.filter(ProjectUUID=item['ProjectUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                out_cheack = ['SourceUrl', 'Project_Introduce', "CheackTimeLatest"]
                for key in item:
                    if (self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key))) and (
                        key not in out_cheack):
                        exist_flag = 'diff'
                        break
            if exist_flag == 'same': item = res_object
            return exist_flag, item

        elif isinstance(item, Building_Detail_Item):
            res_object = q_object.filter(BuildingUUID=item['BuildingUUID']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                out_cheack = ['SourceUrl', 'Project_Introduce', "CheackTimeLatest"]
                for key in item:
                    if (self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key))) and (
                        key not in out_cheack):
                        exist_flag = 'diff'
                        break
            if exist_flag == 'same': item = res_object
            return exist_flag, item

        elif isinstance(item, Certificate_Detail_Item):
            res_object = q_object.filter(PresalePermitNumberUUID=item['PresalePermitNumberUUID']).latest(
                field_name='RecordTime')
            if res_object:
                exist_flag = 'same'
                out_cheack = ['SourceUrl', 'Project_Introduce', "CheackTimeLatest"]
                for key in item:
                    if (self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key))) and (
                        key not in out_cheack):
                        exist_flag = 'diff'
                        break
            if exist_flag == 'same': item = res_object
            return exist_flag, item

        elif isinstance(item, Monitor_Item):
            res_object = q_object.filter(riqi=item['riqi']).latest(field_name='RecordTime')
            if res_object:
                exist_flag = 'update'
                for i in item:
                    res_object[i] = item[i]
                item = res_object
            return exist_flag, item

    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['RecordTime'] = str(datetime.datetime.now())
            item.save()
            # logger.debug("storage item: %(item)s",
            #              {'item': item})

    def process_item(self, item, spider):

        if item:
            status, cheack_item = self.check_item_change(item)
            if status == 'same':
                # 跟踪爬取情况,减少读写注释掉,有需要再开启
                # cheack_item.CheackTimeLatest = str(datetime.datetime.now())
                # cheack_item.save()
                logger.debug("item: %(item)s cheack over", {'item': cheack_item})
            elif status == 'diff':
                self.storage_item(cheack_item)
                logger.debug("item: %(item)s changed", {'item': cheack_item})
            elif status == 'update':
                cheack_item.CheackTimeLatest = str(datetime.datetime.now())
                cheack_item.save()
                logger.debug("item: %(item)s update", {'item': cheack_item})
            elif status == False:
                self.storage_item(cheack_item)
                logger.debug("item: %(item)s  meet first", {'item': cheack_item})





