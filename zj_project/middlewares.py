import logging
import random
from typing import Dict

import pymongo
from scrapy import signals


class ZjProjectSpiderMiddleware:
    '''
    处理
    '''
    # 并非所有方法都需要定义。如果未定义方法，
    # scrapy 的行为就如同 spider 中间件不会修改
    # 传递的对象。

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


class ProxyMiddleware:
    '''
    处理代理的情况
    '''

    def __init__(self):
        with open('./proxy_list.txt', mode='rt', encoding='utf8') as f:
            self.proxy_list = [line.strip() for line in f if line]

    def process_request(self, request, spider):
        random_proxy_url = random.choice(self.proxy_list)
        request.meta['proxy'] = 'http://' + random_proxy_url
        request.meta['download_timeout'] = 15
        # localhost proxy
        # request.meta['proxy'] = 'http://127.0.0.1:7897'

        spider.logger.info('process_request \n'
                           'new proxy is {}\n'
                           'request.url is {}'.format(request.meta['proxy'], request.url))
        # 当返回是None时，Scrapy将继续处理该Request，接着执行其他Downloader Middleware的
        return None

    def process_exception(self, request, exception, spider):
        # 处理异常，切换代理
        old_proxy = request.meta['proxy']
        spider.logger.info('process exception.args is {}\n'
                           'old_proxy is {}\n'
                           'url is {}'.format(exception.args, old_proxy, request.url))
        self.proxy_list.remove(old_proxy)
        if not self.proxy_list:
            raise RuntimeError('proxy_list is empty')
        random_proxy_url = random.choice(self.proxy_list)
        request.meta['proxy'] = 'http://' + random_proxy_url
        spider.logger.info('process exception.args is {}\n'
                           'new_proxy is {}\n'
                           'url is {}'.format(exception.args, request.meta['proxy'], request.url))
        return request

    def process_response(self, request, response, spider):
        spider.logger.info('process_response\n'
                           'ok proxy is {}\n'
                           'url is {}'.format(request.meta['proxy'], request.url))
        return response
