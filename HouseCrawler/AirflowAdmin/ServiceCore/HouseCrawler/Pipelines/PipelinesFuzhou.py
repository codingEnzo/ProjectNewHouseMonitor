#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import datetime
import uuid
from HouseCrawler.Items.ItemsFuzhou import *
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


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


    def check_change(self, item, q_object):
        check_item_flag = False
        monitorkeys = {'house_sts'}
        mainmonitorkeys = {'house_sts', 'cansalenum', "cansalehousenum",
                           }
        copymainmonitorkeys = {'house_class', 'house_use_type', 'house_layout',
                               'house_area_pr_yc', 'house_area_pr_tn', 'house_area_pr_ft',
                               'house_area_pr_dx'}
        nowtime = str(datetime.datetime.now())
        changedata = ''
        if q_object:
            q_object.NewCurTimeStamp = nowtime
            if 'ApprovalUrl' in item.keys():
                q_object.ApprovalUrl = item['ApprovalUrl']
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
            if (isinstance(item, HouseBaseItem)) and check_item_flag:
                for key in monitorkeys:
                    if key not in mainmonitorkeys:
                        continue
                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(q_object, key)):
                        item[key + 'Latest'] = getattr(q_object, key)
            item['change_data'] = changedata
            return check_item_flag, item
        else:
            item['change_data'] = 'new'
            check_item_flag = True
            return check_item_flag, item

    def check_item(self, item):
        check_item_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectinfoBaseItem):
            res_object = q_object.filter(projectuuid=item['projectuuid']).latest(field_name='CurTimeStamp')
            res_object.change_data = 'last'
            res_object.save()
            check_item_flag, item = self.check_change(item, res_object)

        elif isinstance(item, ApprovalBaseItem):
            res_object = q_object.filter(Approvalno=item['Approvalno']).latest(field_name='CurTimeStamp')
            check_item_flag, item = self.check_change(item, res_object)

        elif isinstance(item, BuildingBaseItem):
            res_object = q_object.filter(buildingno=item['buildingno']).latest(field_name='CurTimeStamp')
            check_item_flag, item = self.check_change(item, res_object)


        elif isinstance(item, HouseBaseItem):
            res_object = q_object.filter(house_no=item['house_no']).latest(field_name='CurTimeStamp')
            check_item_flag, item = self.check_change(item, res_object)
        else:
            pass
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
            check_item_flag, now_item = self.check_item(item)
            if check_item_flag:
                logger.debug("item: %(item)s change or met first",
                             {'item': now_item})
                self.storage_item(now_item)
            else:
                logger.debug("item: %(item)s UUID existed",
                             {'item': now_item})



