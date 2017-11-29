# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import sys
import logging

import billiard
import math
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from scrapy.crawler import CrawlerRunner, _get_spider_loader
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))


logger = logging.getLogger(__name__)


class Crawler_Run(billiard.Process):
    def __init__(self, spiderName, settings, urlList=None, *args, **kwargs):
        billiard.Process.__init__(self)
        self.crawler_runner = CrawlerRunner(settings)
        self.start_urls = urlList or []
        self.spider_loader = _get_spider_loader(settings)
        self.extra_params = kwargs.copy()
        print(settings.get('SPIDER_MODULES'), self.spider_loader.list())
        if spiderName in self.spider_loader.list():
            self.spider = self.spider_loader.load(spiderName)
        else:
            print("There is no spider names %s" % spiderName)

    def run(self):
        if self.start_urls:
            url_list = list(self.start_urls)
            spider_count = len(url_list) / 16 + bool(len(url_list) % 16)
            if spider_count >= 32:
                spider_count = 32
            url_index_skip = int(math.ceil(len(url_list) / float(spider_count)))
            for url_index in range(0, len(url_list), url_index_skip):
                self.crawler_runner.crawl(self.spider,
                                        start_urls=url_list[url_index:url_index + url_index_skip])
        else:
            self.crawler_runner.crawl(self.spider, **self.extra_params)
        self.d = self.crawler_runner.join()
        self.d.addBoth(lambda _: reactor.stop())
        # reactor.run(installSignalHandlers=False)
        reactor.run()

    def stop(self):
        for c in list(self.crawler_runner.crawlers):
            c.engine.close_spider(c.spider, 'force stop spider {name}'.format(name=c.spider.name))


@shared_task(bind=True, soft_time_limit=3600 * 3.5, default_retry_delay=60, max_retries=1)
def spider_call(self, spiderName, settings=None, urlList=None, **kwargs):

    settings_use = get_project_settings()

    if settings:
        print(settings)
        try:
            for key in settings:
                if isinstance(settings[key], dict) and isinstance(settings_use[key], dict):
                    settings_use[key].update(settings[key])
                elif isinstance(settings[key], list) and isinstance(settings_use[key], list):
                    settings_use[key].extend(settings[key])
                else:
                    settings_use[key] = settings[key]
        except Exception:
            import traceback
            traceback.print_exc()
    print(urlList)
    self.cur = Crawler_Run(spiderName=spiderName,
                           settings=settings_use,
                           urlList=urlList,
                           **kwargs
                           )
    try:
        self.cur.start()
        self.cur.join()

    # 方式改变不用提异常！
    except SoftTimeLimitExceeded:
        logger.info("任务超时！")
        self.cur.terminate()
        self.cur.join()
        return False
    except Exception:
        pass
    logger.info("任务完成！")
    self.cur.terminate()
    self.cur.join()
    return True
