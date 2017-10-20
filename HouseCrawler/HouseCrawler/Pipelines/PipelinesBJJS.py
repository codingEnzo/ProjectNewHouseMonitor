# coding = utf-8
import sys
import os
import logging
import uuid
from HouseCrawler.Items.ItemsBJJS import *
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class BJJSPipeline(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def check_exist(self, item):
        q_object = item.django_model.objects
        if isinstance(item, ProjectBaseItem):
            pass
        elif isinstance(item, ProjectInfoItem):
            pass
        elif isinstance(item, BuildingInfoItem):
            pass
        elif isinstance(item, HouseInfoItem):
            pass

    def process_item(self, item, spider):
        if hasattr(item, 'save') and hasattr(item, 'django_model'):
            item['RecordID'] = uuid.uuid1()
            

            item.save()
        return item
