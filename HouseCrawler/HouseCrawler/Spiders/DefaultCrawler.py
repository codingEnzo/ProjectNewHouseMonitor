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
                    data = json.loads(data_raw.decode())
                except Exception:
                    import traceback
                    traceback.print_exc()
                    continue
                if "source_url" not in data:
                    continue
                req = Request(url=data['source_url'],
                                method=data.get('method') or 'GET',
                                dont_filter=data.get('dont_filter') or True,
                                meta=data['meta'] or {})
                if req:
                    self.logger.debug("Make Request: %s", str(req.__dict__))
                    yield req

    def parse(self, response):
        pass
