# -*- coding: utf-8 -*-
try:
    import logging

    logger = logging.getLogger(__name__)
except Exception:
    import traceback
    traceback.print_exc()


class HouseInfoDownloaderMiddlerware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        verify_sign = request.meta.get('PageType')
        if verify_sign == 'HouseInfo':
            referer = request.meta.get('referer')
            if referer:
                import requests as req
                req.get(referer, cookies=request.meta.get('cookie'))
                logger.debug('Activate On HouseInfoZS')
