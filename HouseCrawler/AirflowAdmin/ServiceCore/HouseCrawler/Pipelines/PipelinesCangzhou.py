#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import uuid

import datetime
from HouseCrawler.Items.ItemsCangzhou import *
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class Pipeline(object):

    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.njhouse.com.cn",
            'Cache-Control': "max-age=0",
        }


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
    def check_change(self,item,q_object):
        check_item_flag = False
        nowtime = str(datetime.datetime.now())
        monitorkeys = {'HouseSts','HouseBelongSts'}
        mainmonitorkeys = {
            'HouseSts',
            "UnsoldAmount",
            "HouseUnSoldNumber",
            "HouseBelongSts",
            "SellSchedule"
        }
        copymainmonitorkeys = {
            "BuildingAres",
            "DistrictName",
            "QualificationNumber",
            "QualificationLevel",
            "soldAmount",
            "UnsoldAmount",
            "soldAreas",
            "UnsoldAreas",
            "soldAddress",
            "soldPhonNumber",
            "CurrentMonthHouseSoldNumber",
            "CurrentMonthHouseSoldAreas",
            "CurrentMonthBusinessSoldNumber",
            "CurrentMonthBusinessSoldAres",
            "CurrentMonthOtherSoldNumber",
            "TotalHouseSoldNumber",
            "TotalHouseSoldAreas",
            "TotalBusinessSoldNumber",
            "TotalBusinessSoldAres",
            "TotalOtherSoldNumber",
            "HouseUnSoldNumber",
            "HouseUnSoldAreas",
            "BusinessUnSoldNumber",
            "BusinessUnSoldAres",
            "OtherUnSoldNumber",
            "HouseCode",
            "presellInfoCode",
            "buildInfoCode",
            "tdzInfoCode",
            "sgxkzInfoCode",
            "ghxkzInfo",
            "jsydghxkzInfoCode",
            "HouseFloor",
            "HouseNature",
            "HouseUseType",
            "UnitShape",
            "BuildingStructure",
            "ForecastBuildingArea",
            "MeasuredBuildingArea",
            "ForecastInsideOfBuildingArea",
            "MeasuredInsideOfBuildingArea",
            "ForecastPublicArea",
            "MeasuredSharedPublicArea",
            "Address",
        }
        changedata = ''
        if q_object:
            q_object.NewCurTimeStamp = nowtime
            q_object.save()
            for key in item:
                if not hasattr(q_object, key):
                    check_item_flag = True
                    break
                if key not in mainmonitorkeys:
                    continue
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(q_object, key)):
                    changedata = changedata + 'now' + key + ':' + str(item.get(key)) + ',' \
                                 + 'last' + key + ':' + str(getattr(q_object, key)) + ';'
                    check_item_flag = True
                if check_item_flag:
                    for nowkey in item:
                        if nowkey in copymainmonitorkeys:
                            if self.safe_format_value(getattr(q_object, nowkey)).strip() != "" \
                                    and self.safe_format_value(item.get(key)).strip() == "":
                                item[nowkey] = getattr(q_object, nowkey)
            if isinstance(item, HouseBaseItem) and check_item_flag:
                for key in monitorkeys:
                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(q_object, key)):
                        item[key + 'Latest'] = getattr(q_object, key)
            item['change_data'] = changedata
            return check_item_flag, item
        else:
            check_item_flag = True
            return check_item_flag, item

    def check_item(self, item):
        check_item_flag=False
        q_object = item.django_model.objects
        try:
            if isinstance(item, ProjectBaseItem):
                res_object = q_object.filter(ProjectNo=item['ProjectNo']).latest(field_name='CurTimeStamp')
                check_item_flag,item =self.check_change(item,res_object)
        except:
            logging.debug('No ProjectBaseItem')
        try:
            if isinstance(item, PresaleBaseItem):
                res_object = q_object.filter(PresaleNo=item['PresaleNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug('No PresaleBaseItem')

        try:
            if isinstance(item, DeveloperBaseItem):
                res_object = q_object.filter(DeveloperNo=item['DeveloperNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug('No DeveloperBaseItem')


        try:
            if isinstance(item, HouseBaseItem):
                res_object = q_object.filter(HouseNo=item['HouseNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)

        except:
            logging.debug('No HouseBaseItem')

        try:
            if isinstance(item, LandBaseItem):
                res_object = q_object.filter(LandNo=item['LandNo']).latest(field_name='CurTimeStamp')
                check_item_flag, now_item = self.check_change(item, res_object)
        except:
            logging.debug("No LandBaseItem")

        try:
            if isinstance(item, PlanningBaseItem):
                res_object = q_object.filter(PlanningNo=item['PlanningNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug("No PlanningBaseItem")

        try:
            if isinstance(item, ConstructionBaseItem):
                res_object = q_object.filter(ConstructionNo=item['ConstructionNo']).latest(field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug("No ConstructionBaseItem")

        try:
            if isinstance(item, ConstructionLandPlanningBaseItem):
                res_object = q_object.filter(ConstructionLandPlanningNo=item['ConstructionLandPlanningNo']).latest(
                    field_name='CurTimeStamp')
                check_item_flag, item = self.check_change(item, res_object)
        except:
            logging.debug("No ConstructionLandPlanningBaseItem")

        return check_item_flag, item


    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['CurTimeStamp'] = str(datetime.datetime.now())
            item.save()
            logger.debug("storage item: %(item)s",
                         {'item': item})

    def process_item(self, item, spider):
        if item:
            check_item_flag,now_item = self.check_item(item)
            if check_item_flag:
                logger.debug("item: %(item)s change or met first",
                             {'item': now_item})
                self.storage_item(now_item)
            else:
                logger.debug("item: %(item)s UUID existed",
                             {'item': now_item})


