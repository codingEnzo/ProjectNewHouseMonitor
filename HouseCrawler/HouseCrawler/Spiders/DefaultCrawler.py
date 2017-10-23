# coding = utf-8
import time
import json
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from scrapy_redis import connection
from scrapy import signals

DEFAULT_START_URLS_BATCH_SIZE = 8
DEFAULT_START_URLS_KEY = '%(name)s:start_urls'


class DefaultcrawlerSpider(RedisSpider):

    name = "DefaultCrawler"

    def setup_redis(self, crawler=None):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if self.server is not None:
            return

        if crawler is None:
            # We allow optional crawler argument to keep backwards
            # compatibility.
            # XXX: Raise a deprecation warning.
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        settings = crawler.settings

        self.redis_key = settings.get('Redis_key')

        if self.redis_key is None:
            self.redis_key = settings.get(
                'REDIS_START_URLS_KEY', DEFAULT_START_URLS_KEY,
            )

        self.redis_key = self.redis_key % {'name': self.name}

        if not self.redis_key.strip():
            raise ValueError("redis_key must not be empty")

        if self.redis_batch_size is None:
            self.redis_batch_size = settings.getint(
                'REDIS_START_URLS_BATCH_SIZE', DEFAULT_START_URLS_BATCH_SIZE,
            )

        try:
            self.redis_batch_size = int(self.redis_batch_size)
        except (TypeError, ValueError):
            raise ValueError("redis_batch_size must be an integer")

        self.logger.info("Reading start URLs from redis key '%(redis_key)s' "
                         "(batch size: %(redis_batch_size)s)", self.__dict__)

        self.server = connection.from_settings(crawler.settings)
        # The idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def next_requests(self):
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET')
        fetch_one = self.server.spop if use_set else self.server.lpop

        found = 0

        while found < self.redis_batch_size:
            data_raw = fetch_one(self.redis_key)
            if not data_raw:
                break
            data = json.loads(data_raw.decode())
            if "source_url" not in data:
                break
            req = Request(url=data['source_url'],
                            method='GET',
                            dont_filter=True,
                            meta=data['meta'])
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %s", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)

    def parse(self, response):
        pass
