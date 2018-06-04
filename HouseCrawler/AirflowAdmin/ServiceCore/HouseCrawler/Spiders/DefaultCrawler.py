# coding = utf-8
import json

import scrapy
from scrapy.http import Request


class DefaultcrawlerSpider(scrapy.Spider):

    name = "DefaultCrawler"

    def start_requests(self):
        if self.start_urls:
            for data_raw in self.start_urls:
                if not data_raw:
                    continue
                try:
                    data = data_raw if isinstance(data_raw,
                                                  dict) else json.loads(
                                                      str(data_raw))
                except Exception:
                    import traceback
                    traceback.print_exc()
                    continue
                if "source_url" not in data and "url" not in data:
                    continue
                req = Request(
                    url=data.get('source_url') or data.get('url'),
                    method=data.get('method') or 'GET',
                    body=data.get('body'),
                    headers=data.get('headers') or
                    self.crawler.settings.getdict('DEFAULT_REQUEST_HEADERS'),
                    dont_filter=data.get('dont_filter') or True,
                    cookies=data.get('cookies'),
                    meta=data['meta'] or {})
                if req:
                    self.logger.debug("Make Request: %s, %s, %s" %
                                      (req.url, req.body, req.meta))
                    yield req

    def parse(self, response):
        pass
