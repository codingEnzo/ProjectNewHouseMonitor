# coding = utf-8
import json
import sys
import os
import logging
import uuid
import datetime

import django_mongoengine
import redis
import scrapy
from HouseCrawler.Items.ItemsXuzhou import *
from HouseNew.models import *

import base64
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.pipelines.files import FilesPipeline, os


sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class PipelineXuzhou(object):
    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host = self.settings.get('REDIS_HOST'), port = self.settings.get('REDIS_PORT'))

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
        if isinstance(item, ProjectInfoItem):
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
        return exist_flag

    def check_item_change(self, item):
        diff_flag = False
        q_object = item.django_model.objects
        if isinstance(item, ProjectInfoItem):
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
            logger.debug("storage item: %(item)s",
                         {'item': item})

    def replace_str(self, item):
        for key in item:
            if key == 'CurTimeStamp':
                continue
            field = item.django_model._meta.get_field(key)
            if isinstance(field, django_mongoengine.fields.StringField):
                try:
                    if item[key]:
                        value = str(item[key])
                        item[key] = value.replace(u'\xa0', u' ').replace(' ', '').replace('\r', '') \
                            .replace('\t', '').replace('\n', '').replace('　', '').strip()
                    else:
                        item[key] = ''
                except:
                    item[key] = ''

    def process_item(self, item, spider):
        self.replace_str(item)
        if item:
            if isinstance(item,UnitshapeImageInfoItem):
                if len(item.get('ImageFiles'))==0:
                    return item
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


class ImageFilePipeline(FilesPipeline):


    def item_completed(self, results, item, info):
        if not isinstance(item, UnitshapeImageInfoItem):
            return item
        ImageFiles = []
        for ok, x in results:
            if ok:
                with open('/tmp/' + x['path'], 'rb') as f:
                    ImageBase64 = base64.b64encode(f.read())
                    ImageFiles.append(ImageBase64)
                    f.close()
        item['ImageFiles'] = ImageFiles
        return item

    def get_media_requests(self, item, info):
        if isinstance(item, UnitshapeImageInfoItem):
            if item.get('ImageUrls') is None:
                return item
            res_object = item.django_model.objects.filter(HouseUUID=item['HouseUUID']).latest(field_name='CurTimeStamp')
            if res_object is None:
                for fileUrl in item['ImageUrls']:
                    yield scrapy.Request(fileUrl)

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('FilesPipeline.file_key(url) method is deprecated, please use '
                          'file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from file_key with url as first argument
        if not isinstance(request, scrapy.Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() method has been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        ## end of deprecation warning block

        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        media_ext = '.jpg'  # 固定后缀
        return 'full/%s%s' % (media_guid, media_ext)