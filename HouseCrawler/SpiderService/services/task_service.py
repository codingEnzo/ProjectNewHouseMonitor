# -*-coding=utf-8-*-
import pymongo
import functools
from redis import Redis
from collections import deque
from celery import shared_task
from monitor_service import monitor_post
from spider_service import spider_call

redis_client = Redis(host='10.30.1.20')
mongo_col = (pymongo.MongoClient('10.30.1.12'))['ProxyDB']['ProxyIpPool']


def _get_ip_from_api(api, maxsize=100):
    try:
        url_response = mongo_col.find_one({'SourceName': api})['ProxyList']
        if url_response == []:
            return []
        url_queue = deque(redis_client.smembers(api), maxlen=min(maxsize, len(url_response) * 4))
        for item in url_response:
            redis_client.sadd(api, item)
            url_queue.append(item)
        return list(url_queue)
    except Exception:
        import traceback
        traceback.print_exc()
        return []


def just_one_instance(func):
    '''
    装饰器
    如果已经有实例在跑则退出
    :return:
    '''
    @functools.wraps(func)
    def f(*args, **kwargs):
        import socket
        try:
            global s
            s = socket.socket()
            host = socket.gethostname()
            s.bind((host, 60223))
        except Exception:
            print('already has an instance')
            return None
        return func(*args, **kwargs)
    return f


@shared_task(bind=True, queue='spiderQueue')
def bindIpBeat(self):
    spider_call('Yun16spider')
    spider_call('Zdayespider')


@shared_task(bind=True, queue='masterLocal')
@just_one_instance
def getProxyBeat(self):
    spider_call('Getproxyipspider')


@shared_task(bind=True, queue='masterLocal')
def getBindIpBeat(self):
    spider_call('Getbindipspider')


@shared_task(bind=True)
def mergeProxyLow(self):
    try:
        url_list = []
        for api in ['zdaye', 'baizhongsou', '16yun']:
            if 'baizhongsou' in api:
                url_get = _get_ip_from_api(api, maxsize=1500)
            elif '16yun' in api:
                url_get = _get_ip_from_api(api, maxsize=80)
            elif 'zdaye' in api:
                url_get = _get_ip_from_api(api, maxsize=150)
            url_list.extend(url_get)
        url_list = list(set(url_list))
        if len(url_list) == 0:
            raise Exception("all api sources error ")
        redis_client.delete('GZYF_Test:Proxy_Pool')
        for item in url_list:
            redis_client.sadd('GZYF_Test:Proxy_Pool', item)
    except Exception:
        import traceback
        message = traceback.format_exc()
        monitor_post(Action="error", Src='fangtianxia',
                        Instance='ProxyService2', Msg=message)


@shared_task(bind=True)
def mergeProxyMiddle(self):
    try:
        url_list = []
        for api in ['zdaye', '16yun', 'baizhongsou']:
            if 'baizhongsou' in api:
                url_get = _get_ip_from_api(api, maxsize=500)
            elif '16yun' in api:
                url_get = _get_ip_from_api(api, maxsize=75)
            else:
                url_get = _get_ip_from_api(api)
            url_list.extend(url_get)
        url_list = list(set(url_list))
        if len(url_list) == 0:
            raise Exception("all api sources error ")
        redis_client.delete('GZYF_Test:Proxy_Pool:M')
        for item in url_list:
            redis_client.sadd('GZYF_Test:Proxy_Pool:M', item)
    except Exception:
        import traceback
        message = traceback.format_exc()
        monitor_post(Action="error", Src='fangtianxia',
                        Instance='ProxyService2', Msg=message)


@shared_task(bind=True)
def mergeProxyHigh(self):
    try:
        url_list = []
        for api in ['zdaye', '16yun']:
            if 'baizhongsou' in api:
                url_get = _get_ip_from_api(api, maxsize=500)
            elif '16yun' in api:
                url_get = _get_ip_from_api(api, maxsize=75)
            else:
                url_get = _get_ip_from_api(api)
            url_list.extend(url_get)
        url_list = list(set(url_list))
        if len(url_list) == 0:
            raise Exception("all api sources error ")
        redis_client.delete('GZYF_Test:Proxy_Pool:H')
        for item in url_list:
            redis_client.sadd('GZYF_Test:Proxy_Pool:H', item)
    except Exception:
        import traceback
        message = traceback.format_exc()
        monitor_post(Action="error", Src='fangtianxia',
                        Instance='ProxyService2', Msg=message)


@shared_task(bind=True)
def mergeProxyLow2(self):
    try:
        url_list = []
        for api in ['zdaye', 'baizhongsou']:
            if 'baizhongsou' in api:
                url_get = _get_ip_from_api(api, maxsize=500)
            elif '16yun' in api:
                url_get = _get_ip_from_api(api, maxsize=75)
            else:
                url_get = _get_ip_from_api(api)
            url_list.extend(url_get)
        url_list = list(set(url_list))
        if len(url_list) == 0:
            raise Exception("all api sources error ")
        redis_client.delete('GZYF_Test:Proxy_Pool:L:2')
        for item in url_list:
            redis_client.sadd('GZYF_Test:Proxy_Pool:L:2', item)
    except Exception:
        import traceback
        message = traceback.format_exc()
        monitor_post(Action="error", Src='fangtianxia',
                        Instance='ProxyService2', Msg=message)


@shared_task(bind=True)
def mergeProxyHigh2(self):
    try:
        url_list = []
        for api in ['zdaye', 'baizhongsou']:
            if 'baizhongsou' in api:
                url_get = _get_ip_from_api(api, maxsize=65)
            elif '16yun' in api:
                url_get = _get_ip_from_api(api, maxsize=75)
            else:
                url_get = _get_ip_from_api(api)
            url_list.extend(url_get)
        url_list = list(set(url_list))
        if len(url_list) == 0:
            raise Exception("all api sources error ")
        redis_client.delete('GZYF_Test:Proxy_Pool:H:2')
        for item in url_list:
            redis_client.sadd('GZYF_Test:Proxy_Pool:H:2', item)
    except Exception:
        import traceback
        message = traceback.format_exc()
        monitor_post(Action="error", Src='fangtianxia',
                        Instance='ProxyService2', Msg=message)


@shared_task(bind=True)
def resetProxyList(self):
    try:
        for api in ['zdaye', '16yun', 'baizhongsou']:
            redis_client.delete(api)
    except Exception:
        import traceback
        message = traceback.format_exc()
        monitor_post(Action="error", Src='fangtianxia',
                        Instance='ProxyService2', Msg=message)
