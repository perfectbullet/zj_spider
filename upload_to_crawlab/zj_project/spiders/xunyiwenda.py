from http.client import responses
from random import random

import scrapy


class XunyiwendaSpider(scrapy.Spider):
    name = "xunyiwenda"
    allowed_domains = ["club.xywy.com"]
  #  start_urls = ["https://club.xywy.com/list_answer_{}.htm".format(i) for i in range(1, 2000, 1)]
    start_urls = ["https://club.xywy.com/list_all_{}.htm".format(i) for i in range(1,10000,1)]
    current_url = ''
    def parse(self, response):
        self.current_url = response.url
        divlist = response.xpath('//div[@class="item clearfix"]')
        print(len(divlist))
        for idx, div in enumerate(divlist):
         title_url =  'https://club.xywy.com/'+div.xpath('.//a[@class="fl th"]/@href').extract_first()
         problem = div.xpath('./div[1]/div/a/text()').extract_first().strip()
         reply = div.xpath('./div[2]/p/text()').extract_first()
         doctor = div.xpath('./div[3]/div[2]/div[1]/span[1]/text()').extract_first()
         strength = div.xpath('./div[3]/div[2]/div[2]/text()').extract_first()
         hospital = div.xpath('./div[3]/div[2]/div[1]/span[4]/text()').extract_first()
         item = dict(
            title_url=title_url,
            problem=problem,
            reply=reply,
            doctor=doctor,
            strength=strength,
            hospital=hospital
        )
        yield item

