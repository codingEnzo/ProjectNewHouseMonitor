# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


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
                req.get(referer, cookies=request.meta.get('Cookie'))
                logger.debug('Activate On HouseInfoZS')
