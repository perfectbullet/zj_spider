# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from typing import Dict
import logging
import pymongo
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse, Response


class ZjProjectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        mongo_host = crawler.settings.get('MONGO_HOST')  # 从 settings.py 提取
        mongo_port = crawler.settings.get('MONGO_PORT')
        mongo_user = crawler.settings.get('MONGO_USER')  # 数据库登录需要帐号密码的话
        mongo_psw = crawler.settings.get('MONGO_PSW')
        mongo_db = crawler.settings.get('MONGO_DB')

        s.mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port, username=mongo_user, password=mongo_psw)
        s.mongo_db = s.mongo_client[mongo_db]  # 获得数据库的句柄
        logging.getLogger('pymongo').setLevel(logging.INFO)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        coll = self.mongo_db['{}_crawled_urls'.format(spider.name)]  # 获得collection的句柄

        for r in start_requests:
            one_obj: Dict | None = coll.find_one(filter={'ulr': r.url})
            if not one_obj:
                yield r
            else:
                spider.logger.info("request.url %s, have been crawled", r.url)
                continue

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TimeoutException:
    pass


class ZjProjectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        self.mongo_db = None
        self.mongo_client = None

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        mongo_host = crawler.settings.get('MONGO_HOST') # 从 settings.py 提取
        mongo_port = crawler.settings.get('MONGO_PORT')
        mongo_user = crawler.settings.get('MONGO_USER')  # 数据库登录需要帐号密码的话
        mongo_psw = crawler.settings.get('MONGO_PSW')
        mongo_db = crawler.settings.get('MONGO_DB')
        s.mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port, username=mongo_user, password=mongo_psw)
        s.mongo_db = s.mongo_client[mongo_db]  # 获得数据库的句柄
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # try:
        #     coll = self.mongo_db['{}_crawled_urls'.format(spider.name)]  # 获得collection的句柄
        #     one_obj: Dict | None = coll.find_one(filter={'ulr': request.url})
        #     if not one_obj:
        #         return HtmlResponse(url=request.url, request=request, encoding='utf8', status=200)
        #     else:
        #         spider.logger.info("request.url %s, have been crawled", request.url)
        #         return None
        # except TimeoutException:
        #     return HtmlResponse(url=request.url, request=request, status=500)
        # finally:
        #     spider.logger.info('process_request end...')
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
