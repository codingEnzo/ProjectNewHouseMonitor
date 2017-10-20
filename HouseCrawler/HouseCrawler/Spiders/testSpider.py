# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider


class Defaultcrawler1Spider(CrawlSpider):
    name = 'DefaultCrawler1'
    allowed_domains = []
    start_urls = ['http://www.bjjs.gov.cn/eportal/ui?pageId=393547&systemId=2&categoryId=1&salePermitId=5566894&buildingId=469223']

    def start_requests(self):
        for url in self.start_urls:
            req = Request(url=url, meta={'PageType': 'HouseInfo',
                                            'BuildingName': 'hahahahah',
                                            'ProjectName': 'lalalalallal'})
            yield req

    def parse_item(self, response):
        pass
