# coding = utf-8
import json
import copy
import logging
import os
import sys
import datetime
from kafka import KafkaProducer

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class KafkaPipeline(object):

    def __init__(self, settings):
        self.producer = KafkaProducer(bootstrap_servers='10.30.2.205:9092')
        self.settings = settings
        self.city = settings.get('CITY', '')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def get_kafka_json(self, item):
        item_cls = str(item.__class__).replace(
            "<class '", '').replace("'>", '').split('.')[-1]
        if item_cls in ['ProjectInfoItem', 'PresellInfoItem', 'BuildingInfoItem', 'HouseInfoItem', 'PermitInfoItem']:
            table_name = item_cls
            item = copy.deepcopy(item)
            for key in item:
                item[key] = str(item[key])
            kafka_dict = {}
            extra_dict = {}
            kafka_dict['City'] = self.city
            kafka_dict['TableName'] = table_name
            for key in item.fields_map:
                if item.fields_map.get(key) != '' and item.get(item.fields_map.get(key)):
                    kafka_dict[key] = item.pop(item.fields_map.get(key))
                else:
                    kafka_dict[key] = ""
            for key in item:
                extra_dict['Extra' + key] = json.dumps(item.get(key, '')) if (isinstance(item.get(
                    key, ''), dict) or isinstance(item.get(key, ''), list)) else str(item.get(key, ''))
            kafka_dict['ExtraJson'] = extra_dict
            kafka_dict['RecordTime'] = str(datetime.datetime.now())
            return json.dumps(kafka_dict, ensure_ascii=False).encode()

    def process_item(self, item, spider):
        if item:
            print(self.city)
            kafka_json = self.get_kafka_json(item)
            if kafka_json:
                self.producer.send('kafka_spark', kafka_json)
            return item
