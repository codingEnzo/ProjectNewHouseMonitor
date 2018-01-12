# -*- coding: utf-8 -*-
import sys
import os
import logging
import uuid
from HouseCrawler.Items.ItemsNJ import *
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class NJPipeline(object):

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

    def check_item_exist(self, item):
        exist_flag = False
        q_object = item.django_model.objects
        nowtime = str(datetime.datetime.now())
        try:
            if isinstance(item, HouseBaseItem):
                res_object = q_object.filter(HouseNo=item['HouseNo']).latest(
                    field_name='CurTimeStamp')
                if res_object:
                    res_object.NewCurTimeStamp = nowtime
                    res_object.save()
                    exist_flag = True
                return exist_flag
        except Exception:
            logging.debug("No HouseBaseItem")
        try:
            if isinstance(item, DeveloperBaseItem):
                res_object = q_object.filter(DeveloperNo=item['DeveloperNo']).latest(
                    field_name='CurTimeStamp')
                if res_object:
                    res_object.NewCurTimeStamp = nowtime
                    res_object.save()
                    exist_flag = True
                return exist_flag
        except Exception:
            logging.debug("No DeveloperBaseItem")

        try:
            if isinstance(item, PresaleBaseItem):
                res_object = q_object.filter(PresaleNo=item['PresaleNo']).latest(
                    field_name='CurTimeStamp')
                if res_object:
                    res_object.NewCurTimeStamp = nowtime
                    res_object.save()
                    exist_flag = True
                return exist_flag
        except Exception:
            logging.debug("No PresaleBaseItem")

        try:
            if isinstance(item, ProjectBaseItem):
                res_object = q_object.filter(ProjectNo=item['ProjectNo']).latest(
                    field_name='CurTimeStamp')
                if res_object:
                    res_object.NewCurTimeStamp = nowtime
                    res_object.save()
                    exist_flag = True
                return exist_flag
        except Exception:
            logging.debug("No ProjectBaseItem")

        try:
            if isinstance(item, BuildingBaseItem):
                res_object = q_object.filter(BuildingNo=item['BuildingNo']).latest(
                    field_name='CurTimeStamp')
                if res_object:
                    res_object.NewCurTimeStamp = nowtime
                    res_object.save()
                    exist_flag = True
                return exist_flag
        except Exception:
            logging.debug("No BuildingBaseItem")

    def check_item_change(self, item):
        diff_flag = False
        monitorkeys = {'HouseSts'}
        mainmonitorkeys = {'HouseSts'}
        copymainmonitorkeys = {'ForecastBuildingArea',
                               'ForecastInsideOfBuildingArea', 'ForecastPublicArea'}
        q_object = item.django_model.objects
        try:
            if isinstance(item, ProjectBaseItem):
                res_object = q_object.filter(ProjectNo=item['ProjectNo']).latest(
                    field_name='CurTimeStamp')
                changedata = ''
                for key in item:
                    if key not in mainmonitorkeys:
                        continue
                    if not hasattr(res_object, key):
                        diff_flag = True
                        break

                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                        changedata = changedata + 'now' + key + ':' + str(item.get(key)) + ',' \
                            + 'last' + key + ':' + \
                            str(getattr(res_object, key)) + ';'
                        diff_flag = True
                item['change_data'] = changedata
                return diff_flag, item
        except Exception:
            logging.debug('No ProjectBaseItem')
        try:
            if isinstance(item, PresaleBaseItem):
                res_object = q_object.filter(PresaleNo=item['PresaleNo']).latest(
                    field_name='CurTimeStamp')
                changedata = ''
                for key in item:
                    if key not in mainmonitorkeys:
                        continue
                    if not hasattr(res_object, key):
                        diff_flag = True
                        break

                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                        changedata = changedata + 'now' + key + ':' + str(item.get(key)) + ',' \
                            + 'last' + key + ':' + \
                            str(getattr(res_object, key)) + ';'
                        diff_flag = True
                item['change_data'] = changedata
                return diff_flag, item
        except Exception:
            logging.debug('No PresaleBaseItem')

        try:
            if isinstance(item, DeveloperBaseItem):
                res_object = q_object.filter(DeveloperNo=item['DeveloperNo']).latest(
                    field_name='CurTimeStamp')
                changedata = ''
                for key in item:
                    if key not in mainmonitorkeys:
                        continue
                    if not hasattr(res_object, key):
                        diff_flag = True
                        break

                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                        changedata = changedata + 'now' + key + ':' + str(item.get(key)) + ',' \
                            + 'last' + key + ':' + \
                            str(getattr(res_object, key)) + ';'
                        diff_flag = True
                item['change_data'] = changedata
                return diff_flag, item
        except Exception:
            logging.debug('No DeveloperBaseItem')

        try:
            if isinstance(item, BuildingBaseItem):
                res_object = q_object.filter(BuildingNo=item['BuildingNo']).latest(
                    field_name='CurTimeStamp')
                changedata = ''
                for key in item:
                    if key not in mainmonitorkeys:
                        continue
                    if not hasattr(res_object, key):
                        diff_flag = True
                        break
                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                        changedata = changedata + 'now' + key + ':' + str(item.get(key)) + ',' \
                            + 'last' + key + ':' + \
                            str(getattr(res_object, key)) + ';'
                        diff_flag = True
                item['change_data'] = changedata
                return diff_flag, item
        except Exception:
            logging.debug('No BuildingBaseItem')

        try:
            if isinstance(item, HouseBaseItem):
                res_object = q_object.filter(HouseNo=item['HouseNo']).latest(
                    field_name='CurTimeStamp')
                changedata = ''
                for key in item:
                    if key not in mainmonitorkeys:
                        continue
                    if not hasattr(res_object, key):
                        diff_flag = True
                        break

                    if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                        changedata = changedata + 'now' + key + ':' + str(item.get(key)) + ',' \
                            + 'last' + key + ':' + \
                            str(getattr(res_object, key)) + ';'
                        diff_flag = True
                item['change_data'] = changedata
                if diff_flag:
                    try:
                        if self.safe_format_value(item.get('HouseSts')) != self.safe_format_value(
                                getattr(res_object, 'HouseSts')):
                            for nowkey in copymainmonitorkeys:
                                item[nowkey] = getattr(res_object, nowkey)
                    except Exception:
                        print('存储失败')
                    for key in monitorkeys:
                        item[key + 'Latest'] = getattr(res_object, key)
                return diff_flag, item
        except Exception:
            logging.debug('No HouseBaseItem')

    def storage_item(self, item):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            item['CurTimeStamp'] = str(datetime.datetime.now())
            item.save()
            logger.debug("storage item: %(item)s",
                         {'item': item})

    def process_item(self, item, spider):
        if item:
            item_exist_flag = self.check_item_exist(item)
            if item_exist_flag:
                logger.debug("item: %(item)s UUID existed",
                             {'item': item})
                diff_result, diff_item = self.check_item_change(item)
                if diff_result:
                    self.storage_item(diff_item)
            else:
                logger.debug("item: %(item)s met first",
                             {'item': item})
                self.storage_item(item)
            return item
