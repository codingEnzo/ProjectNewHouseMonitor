# -*- coding: utf-8 -*-
try:
    import logging

    logger = logging.getLogger(__name__)
except Exception:
    import traceback
    traceback.print_exc()


class CookiesDownloaderMiddleware(object):

    def __init__(self, crawler):
        self.settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        import requests as req
        authURL = 'http://61.146.213.163:8011/user_kfs.aspx'
        proxy = request.meta.get('proxy')
        res = req.get(authURL, header=request.headers, proxies={'http': proxy, 'https': proxy}, timeout=5)
        request.headers.setdefault('Cookie', 'ASP.NET_SessionId: %s' % res.cookies.get('ASP.NET_SessionId', ''))
        logger.debug('Activate On Zhaoqing')
