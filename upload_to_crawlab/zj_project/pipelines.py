import hashlib
import os
import random
import sqlite3
from typing import Dict

import pymongo
import requests
import scrapy

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import ftplib
import requests
from PIL import Image
# python2.x, use this instead
# from StringIO import StringIO
# for python3.x,
from io import StringIO, BytesIO

image_dir = 'image_dir'
settings = get_project_settings()


class ZjProjectPipeline:
    def __init__(self, FTP_HOST, FTP_USER, FTP_PASS):
        # connect to the FTP server
        self.ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        # force UTF-8 encoding
        # ftp.encoding = "utf-8"
        with open('./proxy_list.txt', mode='rt', encoding='utf8') as f:
            self.proxy_list = [line.strip() for line in f if line]

    @classmethod
    def from_crawler(cls, crawler):
        FTP_HOST = crawler.settings.get('FTP_HOST')
        FTP_USER = crawler.settings.get('FTP_USER')
        FTP_PASS = crawler.settings.get('FTP_PASS')
        return cls(FTP_HOST, FTP_USER, FTP_PASS)

    def upload(self, response):
        # local file name you want to upload
        image_url_hash = hashlib.shake_256(response.url.encode()).hexdigest(5)
        image_perspective = response.url.split("/")[-2]
        image_filename = f"{image_url_hash}_{image_perspective}.jpg"

        with BytesIO(response.content) as f:
            with Image.open(f) as image:
                # converting to jpg
                rgb_image = image.convert("RGB")
                rgb_image.save('tmp.jpg')
                with open('tmp.jpg', "rb") as file:
                    # use FTP's STOR command to upload the file
                    self.ftp.storbinary(f"STOR images/{image_filename}", file)
                    return image_filename

    def process_item(self, item, spider):
        for proxy_url in self.proxy_list:
            proxies = {
                # 'http': 'http://' + proxy_url,
                'https': 'http://' + proxy_url,
            }
            try:
                # response = requests.get(item['image_urls'][0], proxies=proxies)
                image_url = item['image_urls'][0]
                response = requests.get(image_url, proxies=proxies, stream=True)
                if response.status_code == 200:
                    # spider.logger.info(
                    #     'ZjProjectPipeline item {}, proxies is {}, response is {}'.format(item, proxies, response))
                    image_filename = self.upload(response)
                    spider.logger.info('ZjProjectPipeline upload {} to ftp'.format(image_filename))
                    item['image_filename'] = image_filename
                    return item
            except Exception as e:
                spider.logger.info('ZjProjectPipeline Exception is {}'.format(e))
        return item


class SaveAirlineImage:
    def process_item(self, item, spider):
        image_name = item['image_url'].split('/')[-1]
        if spider.name == 'airlines':
            image_dir = 'image_dir/AirlineImage'
        else:
            image_dir = 'image_dir/{}'.format(spider.name)
        if os.path.normcase(image_dir):
            os.makedirs(image_dir, exist_ok=True)
        image_path = '{}/{}'.format(image_dir, image_name)
        if not os.path.exists(image_path):
            try:
                response = requests.get(item['image_url'])
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                item['image_path'] = image_path
                spider.logger.info('image_path is {}'.format(image_path))
                return item
            except Exception as e:
                item['image_path'] = ''
                return item
                print('error is {}'.format(e))
        else:
            item['image_path'] = image_path
            print('image_path is been saved {}'.format(image_path))
            return item


class Sqlite3Pipeline(object):

    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table

    @classmethod
    def from_crawler(cls, crawler):
        sqlite_table = crawler.spider.name
        return cls(
            sqlite_file=crawler.settings.get('SQLITE_FILE'),  # 从 settings.py 提取
            sqlite_table=sqlite_table
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        CREATE_TABLE = f'''CREATE TABLE IF NOT EXISTS airline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image_url TEXT NOT NULL UNIQUE,
        image_path TEXT NOT NULL,
        air_force TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL
        )'''
        self.conn.execute(CREATE_TABLE)
        CREATE_TABLE = f'''CREATE TABLE IF NOT EXISTS {self.sqlite_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                title_url TEXT NOT NULL UNIQUE,
                image_url TEXT NOT NULL,
                image_path TEXT NOT NULL,
                date TEXT NOT NULL,
                brand TEXT NOT NULL,
                feature TEXT NOT NULL,
                factory TEXT NOT NULL,
                category TEXT NOT NULL,
                zczh TEXT NOT NULL,
                zsdw TEXT NOT NULL,
                scdw TEXT NOT NULL,
                syks TEXT NOT NULL,
                cpfl TEXT NOT NULL,
                cpyt TEXT NOT NULL,
                cpsm TEXT NOT NULL
                )'''
        self.conn.execute(CREATE_TABLE)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        insert_sql = "insert into {0}({1}) values ({2})".format(self.sqlite_table,
                                                                ','.join(item.fields.keys()),
                                                                ','.join(['?'] * len(item.fields.keys())))
        args_list = [item[k] for k in item.fields.keys()]
        self.cur.execute(insert_sql, args_list)
        self.conn.commit()
        with open('{}_crawled_urls.txt'.format(spider.name), mode='r+', encoding='utf8') as f:
            old_lines = {line.strip() for line in f.readlines()}
            if spider.current_url not in old_lines:
                f.write(spider.current_url + '\n')
        return item


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


class MyImagePipeline(ImagesPipeline):
    '''
    Custom File Naming
    '''

    def file_path(self, request, response=None, info=None, *, item=None):
        image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        image_perspective = request.url.split("/")[-2]
        image_filename = f"{image_url_hash}_{image_perspective}.jpg"
        # print('{}\nimage_filename is {}'.format('*' * 100, image_filename))
        info.spider.logger.info('{}\nfile_path request meta is {}'.format('*' * 100, request.meta))
        return image_filename

    def get_media_requests(self, item, info):
        meta = {'proxy': ''}
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta=meta)
