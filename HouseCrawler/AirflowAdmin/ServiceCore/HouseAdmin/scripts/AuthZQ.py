# -*- coding: utf-8 -*-
import redis
import requests as req


def run():
    r = redis.Redis('10.30.1.20')
    while True:
        try:
            authURL = 'http://61.146.213.163:8011/user_kfs.aspx'
            res = req.get(authURL, timeout=10)
            r.set('ZQSID', 'ASP.NET_SessionId: %s' %
                  res.cookies.get('ASP.NET_SessionId', ''))
            print(res.cookies.get('ASP.NET_SessionId', ''))
        except Exception:
            import traceback
            traceback.print_exc()
