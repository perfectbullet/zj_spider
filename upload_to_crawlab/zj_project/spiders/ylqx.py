from typing import Any

import scrapy
from scrapy.http import Request, Response
from zj_project.items import YlqxItem

class YlqxSpider(scrapy.Spider):
    name = "ylqx"
    allowed_domains = ["ylqx.qgyyzs.net"]
    start_urls = ["https://ylqx.qgyyzs.net/zs/list_0_0_0_{}.htm".format(i) for i in range(1, 2754, 1)]
    current_url = ""
    # def start_requests(self):
    #     HTTP_PROXY = 'http://127.0.0.1:7897'  # 替换为你的代理IP
    #     for url in self.start_urls:
    #         # yield scrapy.Request(url, meta={'proxy': HTTP_PROXY})
    #         yield scrapy.Request(url)

    def parse(self, response: Response) -> Any:
        self.current_url = response.url
        div_list = response.xpath('//div[@class="r_list"]')
        self.logger.info('*******************length of divList is {}*******************'.format(len(div_list)))
        for idx, div in enumerate(div_list, start=1):
            # . 选取当前节点。 <a href="/search?aircraft=25083&amp;display=detail">
            # //*[@id="layout-page"]/div[2]/section/section/section/div/section[2]/div/div[1]/div/div[1]/div[2]/div
            title = div.xpath('./dl/dt[1]/a[1]/@title').extract_first().strip()
            title_url = 'https://' + self.allowed_domains[0] + div.xpath('./dl/dt[1]/a[1]/@href').extract_first().strip()
            image_url = div.xpath('./a[1]/@rel').extract_first().strip()
            date = div.xpath('./dl/dd[3]/text()').extract_first()
            brand = div.xpath('./dl/dt[2]/text()').extract_first()
            feature = div.xpath('./dl/dt[3]/text()').extract_first()
            factory = div.xpath('./dl/dd[1]/a[1]/@title').extract_first()
            category = div.xpath('./dl/dd[2]/a/text()').extract_first()
            item = YlqxItem(title=title,
                            title_url=title_url,
                            image_url=image_url,
                            date=date,
                            brand=brand,
                            feature=feature,
                            factory=factory,
                            category=category
                            )
            yield scrapy.Request(url=title_url, callback=self.sec_handler, meta={'item': item}, priority=1)


    def sec_handler(self, response:Response):
        item = response.meta['item']
        # 获取子页面内容
        right_v = response.xpath('//div[@class="right_v"]')
        r_mina = response.xpath('//div[@class="r_mina"]')
        # 注册证号
        item['zczh'] = r_mina.xpath('./dl[3]/dd[1]/text()').extract_first().strip()
        # 招商单位
        item['zsdw'] = r_mina.xpath('./dl[4]/dd[1]/text()').extract_first().strip()
        # 生产单位
        item['scdw'] = r_mina.xpath('./dl[5]/dd[1]/text()').extract_first().strip()
        # 使用科室
        item['syks'] = ','.join([a.xpath('./text()').extract_first() for a in r_mina.xpath('./dl[7]/dd/a')])
        # 产品分类
        item['cpfl'] = ','.join([a.xpath('./text()').extract_first() for a in r_mina.xpath('./dl[8]/dd[1]/a')])
        # 产品用途
        item['cpyt'] = right_v.xpath('./div[4]/dl[1]/dd/text()').extract_first()
        # 产品说明
        item['cpsm'] = right_v.xpath('./div[5]/dl[1]/dd[1]/text()').extract_first()
        return item
