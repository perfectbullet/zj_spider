# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZjProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AirlineItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()  # 封面图片链接
    name = scrapy.Field()  # 飞机名称
    image_path = scrapy.Field()  # 图片地址
    date = scrapy.Field()
    location = scrapy.Field()
    air_force = scrapy.Field()

class AirlineItemv3(scrapy.Item):
    '''
    image download
    '''
    # define the fields for your item here like:
    image_urls = scrapy.Field()  # 图片链接
    name = scrapy.Field()  # 飞机名称
    image_path = scrapy.Field()  # 图片地址
    date = scrapy.Field()
    location = scrapy.Field()
    air_force = scrapy.Field()

class YlqxItem(scrapy.Item):
    title = scrapy.Field() # 标题
    title_url = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
    date = scrapy.Field()
    brand = scrapy.Field()
    feature = scrapy.Field()
    factory = scrapy.Field()
    category = scrapy.Field()
    # 子页面内容
    # 注册证号
    zczh = scrapy.Field()
    # 招商单位
    zsdw = scrapy.Field()
    # 生产单位
    scdw = scrapy.Field()
    # 使用科室
    syks = scrapy.Field()
    # 产品分类
    cpfl = scrapy.Field()
    # 产品用途
    cpyt = scrapy.Field()
    # 产品说明
    cpsm = scrapy.Field()