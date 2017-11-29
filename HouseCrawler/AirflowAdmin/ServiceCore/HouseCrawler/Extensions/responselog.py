# coding=utf-8
import copy
import datetime
import pymongo
from scrapy import signals
from DownloaderBin.settings import proxy_stat_update


class ResponseLog(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.mongo_client = pymongo.MongoClient("192.168.6.204", 27017)
        self.response_log_col = self.mongo_client['HouseCrawler']['ScrapyDownloaderLog']
        cs = self.crawler.signals
        cs.connect(self._request_scheduled, signal=signals.request_scheduled)
        cs.connect(self._request_dropped, signal=signals.request_dropped)
        cs.connect(self._response_received, signal=signals.response_received)

    def _check_connection(self):
        try:
            cur_time = datetime.datetime.now()
            result = self.response_log_col.find_and_modify(query={'URL':"TEST_INDEX"},
                                                    update={'$set':{'STATUS':'ENABLED', 'MODIFIED_AT':cur_time}},
                                                    new=True)
            if not result:
                self.response_log_col.insert_one({'URL':'TEST_INDEX','STATUS':'ENABLED', 'MODIFIED_AT':cur_time})
        except Exception:
            try:
                self.mongo_client.close()
                del self.mongo_client
                del self.response_log_col
            except Exception:
                pass
            self.mongo_client = pymongo.MongoClient("192.168.6.204", 27017)
            self.response_log_col = self.mongo_client['HouseCrawler']['ScrapyDownloaderLog']

    def _response_received(self, response, request, spider, *args, **kwargs):
        cur_time = datetime.datetime.now()
        self._check_connection()
        result = self.response_log_col.find_and_modify(query={'URL':response.url},
                                                update={'$set':{'STATUS':response.status, 'MODIFIED_AT':cur_time}},
                                                new=True)
        if not result:
            new_dict = copy.deepcopy(response.meta['logInfo'])
            new_dict.update({'URL':response.url,'STATUS':response.status, 'MODIFIED_AT':cur_time})
            self.response_log_col.insert_one(new_dict)

    def _request_scheduled(self, request, spider, *args, **kwargs):
        cur_time = datetime.datetime.now()
        self._check_connection()
        result = self.response_log_col.find_and_modify(query={'URL':request.url},
                                                update={'$set':{'STATUS':'scheduled', 'MODIFIED_AT':cur_time}},
                                                new=True)
        if not result:
            new_dict = copy.deepcopy(request.meta['logInfo'])
            new_dict.update({'URL':request.url, 'STATUS':'scheduled', 'MODIFIED_AT':cur_time})
            self.response_log_col.insert_one(new_dict)

    def _request_dropped(self, request, spider, *args, **kwargs):
        cur_time = datetime.datetime.now()
        self._check_connection()
        result = self.response_log_col.find_and_modify(query={'URL':request.url},
                                                update={'$set':{'STATUS':'dropped', 'MODIFIED_AT':cur_time}},
                                                new=True)
        if not result:
            new_dict = copy.deepcopy(request.meta['logInfo'])
            new_dict.update({'URL':request.url, 'STATUS':'dropped', 'MODIFIED_AT':cur_time})
            self.response_log_col.insert_one(new_dict)
