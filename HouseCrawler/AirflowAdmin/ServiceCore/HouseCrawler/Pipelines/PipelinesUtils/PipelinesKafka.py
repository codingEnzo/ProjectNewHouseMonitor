# coding = utf-8
import json
import logging
import os
import sys
from kafka import KafkaProducer

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class KafkaPipeline(object):

    def __init__(self, settings):
        self.producer = KafkaProducer(bootstrap_servers='10.30.2.205:9092')
        self.settings = settings
        self.city = settings.get('CITY')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def get_kafka_json(self, item):
        kafka_dict = {}
        extra_dict = {}
        kafka_dict['City'] = self.city
        for key in item.fields_map:
            if item.fields_map.get(key) != '' and item.get(item.fields_map.get(key)):
                kafka_dict[key] = item.pop(item.fields_map.get(key))
        for key in item:
            extra_dict['Extra' + key] = str(item.get(key, ''))
        kafka_dict['ExtraJson'] = extra_dict
        return json.dumps(kafka_dict).encode()

    def process_item(self, item, spider):
        if item:
            self.producer.send('kafka_spark', self.get_kafka_json(item))
            return item
