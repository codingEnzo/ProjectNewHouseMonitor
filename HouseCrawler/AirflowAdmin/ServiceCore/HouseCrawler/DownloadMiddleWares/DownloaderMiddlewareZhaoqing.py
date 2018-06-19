# -*- coding: utf-8 -*-
try:
    import redis
    import logging

    logger = logging.getLogger(__name__)
except Exception:
    import traceback
    traceback.print_exc()


class CookiesDownloaderMiddleware(object):

    def __init__(self, crawler):
        self.r = redis.Redis(host='10.30.1.20', port=6379)
        self.settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        proxy = request.meta.get('proxy')
        sid = self.r.get(proxy)
        if sid:
            request.headers.setdefault(
                'Cookie', sid.decode())
            logger.debug('Activate On Zhaoqing')
