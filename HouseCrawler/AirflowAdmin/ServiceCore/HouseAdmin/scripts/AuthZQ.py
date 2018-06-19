# -*- coding: utf-8 -*-
import redis
import requests as req


def run():
    r = redis.Redis('10.30.1.20')
    while True:
        proxies = r.smembers('GZYF_Test:Proxy_Pool:H')
        for proxy in proxies:
            proxy_tmp = "http://%s" % proxy.decode()
            authURL = 'http://61.146.213.163:8011/user_kfs.aspx'
            res = req.get(authURL, proxies={
                'http': proxy_tmp, 'https': proxy_tmp}, timeout=5)
            r.set(proxy_tmp, 'ASP.NET_SessionId: %s' %
                  res.cookies.get('ASP.NET_SessionId', ''))
            r.expire(proxy_tmp, 30)
            print(proxy_tmp)
