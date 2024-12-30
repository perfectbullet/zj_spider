import ftplib
import hashlib
from io import BytesIO
from typing import Dict

import pymongo
import requests
from PIL import Image
from scrapy.utils.project import get_project_settings


settings = get_project_settings()


class SaveAirlineImage:
    def __init__(self, FTP_HOST, FTP_USER, FTP_PASS, IMAGES_STORE_DIR):
        # connect to the FTP server
        self.ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        # force UTF-8 encoding
        # ftp.encoding = "utf-8"
        self.images_store_dir = IMAGES_STORE_DIR
        with open('./proxy_list.txt', mode='rt', encoding='utf8') as f:
            self.proxy_list = [line.strip() for line in f if line]

    @classmethod
    def from_crawler(cls, crawler):
        FTP_HOST = settings.get('FTP_HOST')
        FTP_USER = settings.get('FTP_USER')
        FTP_PASS = settings.get('FTP_PASS')
        IMAGES_STORE_DIR = settings.get('IMAGES_STORE_DIR')
        return cls(FTP_HOST, FTP_USER, FTP_PASS, IMAGES_STORE_DIR)

    def upload(self, response):
        # local file name you want to upload
        image_url_hash = hashlib.shake_256(response.url.encode()).hexdigest(5)
        image_perspective = response.url.split("/")[-2]
        image_filename = f"{self.images_store_dir}/{image_url_hash}_{image_perspective}.jpg"

        with BytesIO(response.content) as f:
            with Image.open(f) as image:
                # converting to jpg
                rgb_image = image.convert("RGB")
                rgb_image.save('tmp.jpg')
                with open('tmp.jpg', "rb") as file:
                    # use FTP's STOR command to upload the file
                    self.ftp.storbinary(f"STOR {image_filename}", file)
                    return image_filename

    def process_item(self, item, spider):
        if spider.crawler.settings.get('USE_PROXY'):
            for proxy_url in self.proxy_list:
                proxies = {
                    'http': 'http://' + proxy_url,
                    'https': 'http://' + proxy_url,
                }
                try:
                    # response = requests.get(item['image_urls'][0], proxies=proxies)
                    item['image_filenames'] = []
                    item['local_image_url'] = []
                    for image_url in item['image_urls']:
                        spider.logger.info('SaveAirlineImage proxies is {}, image_url is {}'.format(proxies, image_url))
                        response = requests.get(image_url, proxies=proxies, stream=True)
                        if response.status_code == 200:
                            spider.logger.info(
                                'SaveAirlineImage item {}, proxies is {}, response is {}'.format(item, proxies, response))
                            image_filename = self.upload(response)
                            spider.logger.info('SaveAirlineImage upload {} to ftp'.format(image_filename))
                            item['image_filenames'].appdend(image_filename)
                            item['local_image_url'].appedn('http://localhost:8010/{}'.format(image_filename))
                        else:
                            spider.logger.info('SaveAirlineImage load image not ok {}'.format(response))
                    return item
                except Exception as e:
                    spider.logger.error('SaveAirlineImage Exception is {}'.format(e))
            return item
        else:
            try:
                # response = requests.get(item['image_urls'][0], proxies=proxies)
                item['image_filenames'] = []
                item['local_image_url'] = []
                for image_url in item['image_urls']:
                    spider.logger.info('SaveAirlineImage not proxies , image_url is {}'.format( image_url))
                    response = requests.get(image_url, stream=True)
                    if response.status_code == 200:
                        spider.logger.info(
                            'SaveAirlineImage item {}, not proxies, response is {}'.format(item, response))
                        image_filename = self.upload(response)
                        spider.logger.info('SaveAirlineImage upload {} to ftp'.format(image_filename))
                        item['image_filenames'].appdend(image_filename)
                        item['local_image_url'].appedn('http://localhost:8010/{}'.format(image_filename))
                    else:
                        spider.logger.info('SaveAirlineImage load image not ok {}'.format(response))
                return item
            except Exception as e:
                spider.logger.error('SaveAirlineImage Exception is {}'.format(e))


class MongodbPipeline(object):

    def __init__(self, mongo_host, mongo_port, mongo_user, mongo_psw, mongo_db):
        self.client = pymongo.MongoClient(host=mongo_host, port=mongo_port, username=mongo_user, password=mongo_psw)
        self.db = self.client[mongo_db]  # 获得数据库的句柄
        self.count_pages = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),  # 从 settings.py 提取
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_user=crawler.settings.get('MONGO_USER'),  # 数据库登录需要帐号密码的话
            mongo_psw=crawler.settings.get('MONGO_PSW'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        spider.logger.info("open spider")

    def close_spider(self, spider):
        spider.logger.info("close spider")

    def process_item(self, item, spider):
        # 保存爬取过的页面，去重
        coll = self.db['{}_crawled_urls'.format(spider.name)]  # 获得collection的句柄
        one_obj: Dict | None = coll.find_one(filter={'ulr': spider.current_url})
        if not one_obj:
            coll.insert_one({'ulr': spider.current_url})  # 向数据库插入一条记录
            self.count_pages += 1
        spider.logger.info('self.count_pages is {}'.format(self.count_pages))
        return item
