# -*- coding: utf-8 -*-

import sys
import random
import logging
from redis import Redis
from HouseCrawler.Utils.GetLocalIP import LOCALIP
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


if "192.168.6" in LOCALIP or "10.30.1" in LOCALIP:
    link_env = 'master'
else:
    link_env = 'slave'

r = Redis(host='10.30.1.20', port=6379)

logger = logging.getLogger(__name__)


class RandomUserAgent(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddleware(object):

    def __init__(self, proxy_pool_name):
        self._proxy_pool_name = proxy_pool_name
        self._proxy_pool_map = {'master': {'low': self._proxy_pool_name,
                                            'middle': 'GZYF_Test:Proxy_Pool:M',
                                            'high': 'GZYF_Test:Proxy_Pool:H'},
                                'slave': {'low': 'GZYF_Test:Proxy_Pool:L:2',
                                            'middle': 'GZYF_Test:Proxy_Pool:L:2',
                                            'high': 'GZYF_Test:Proxy_Pool:H:2'}}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('PROXY_POOL_NAME', 'GZYF_Test:Proxy_Pool'))

    def process_request(self, request, spider):
        hostname = urlparse.urlparse(request.url).hostname
        proxy_status = b'True'
        if proxy_status == b'True':
            if 'anjuke' in request.url:
                proxy = r.srandmember(self._proxy_pool_map[link_env]['high'])
            else:
                proxy = r.srandmember(self._proxy_pool_map[link_env]['high'])
            if proxy:
                proxy = proxy.decode('utf-8')
                request.meta['proxy'] = "http://%s" % (proxy)
                logger.debug('{} 代理 {}'.format(request.url, proxy))
        else:
            logger.debug("当前不使用代理")
