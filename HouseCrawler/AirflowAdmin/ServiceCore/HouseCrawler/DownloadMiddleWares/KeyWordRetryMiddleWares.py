"""
An extension to retry failed requests that are potentially caused by temporary
problems such as a connection timeout or HTTP 500 error.

You can change the behaviour of this middleware by modifing the scraping settings:
RETRY_TIMES - how many times to retry a failed page
RETRY_HTTP_CODES - which HTTP response codes to retry

Failed pages are collected on the scraping process and rescheduled at the end,
once the spider has finished crawling all regular (non failed) pages. Once
there is no more failed pages to retry this middleware sends a signal
(retry_complete), so other extensions could connect to that signal.
"""
import sys
import logging
from redis import Redis
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.xlib.tx import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


logger = logging.getLogger(__name__)
r = Redis(host='10.30.1.20', port=6379)


class KeyWordRetryMiddleware(object):

    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)

    def __init__(self, crawler):
        try:
            self.settings = settings = crawler.settings
            self.signals = crawler.signals
            if not settings.getbool('RETRY_ENABLED'):
                raise NotConfigured
            self.max_retry_times = settings.getint('RETRY_TIMES')
            self.retry_keyword = set(str(x)
                                     for x in settings.getlist('RETRY_KEYWORD'))
            self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        except Exception:
            import traceback
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        retry_flag = False
        if request.meta.get('dont_retry', False):
            return response
        for k in self.retry_keyword:
            if k in response.body_as_unicode():
                retry_flag = True
                break
        if retry_flag:
            reason = 'retry with key word'
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        hostname = urlparse.urlparse(request.url).hostname
        r.set(hostname, True)
        r.expire(hostname, time=1800)
        if retries <= self.max_retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            del request
            print('%s retry %s times' % (retryreq.url, retries))
            return retryreq
        else:
            self.signals.send_catch_log(signal=signals.request_dropped,
                                        request=request, spider=spider)
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})