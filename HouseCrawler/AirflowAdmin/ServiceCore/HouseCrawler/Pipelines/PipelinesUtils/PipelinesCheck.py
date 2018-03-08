# coding = utf-8
import sys
import os
import logging
from scrapy.exceptions import DropItem
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class CheckPipeline(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def check_item(self, item):
        exist_flag = False
        blank_count = 0
        for key in item:
            if item.get(key) in (None, ''):
                blank_count += 1
        if blank_count >= 0.8 * len(item):
            exist_flag = True
        return exist_flag

    def process_item(self, item, spider):
        if item:
            if not self.check_item(item):
                return item
            raise DropItem('More then 0.8 of Fields is empty')
