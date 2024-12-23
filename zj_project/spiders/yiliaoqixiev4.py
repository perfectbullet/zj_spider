import scrapy
from tldextract import extract


class Yiliaoqixiev4Spider(scrapy.Spider):
    name = "yiliaoqixiev4"
    allowed_domains = ["www.chinamedevice.cn"]
    start_urls = ["https://www.chinamedevice.cn/product/12/1/{}.html".format(i) for i in range(1,119,1)]

    def parse(self, response):
        lilivst = response.xpath('//div[@class="list"]/ul/li')
        for idx, li in enumerate(lilivst, start=1):
            print('idx is {}'.format(idx))
            mingcheng = li.xpath('./h3/span/a/text()').extract_first().strip() #器械名称
            wenhao = li.xpath('./p[2]/text()').extract_first().strip() #批准文号
            shuoming = li.xpath('./p[3]/text()').extract_first().strip() #产品说明
            company = li.xpath('./p[4]/a[1]/text()').extract_first()      #公司名称
            image_url = li.xpath('./p[1]/a/img/@src').extract_first() #图片链接
            title_url = li.xpath('./p[1]/a/@href').extract_first() #二级页面链接
            item = dict(mingcheng=mingcheng,
                       wenhao=wenhao,
                       shuoming=shuoming,
                       image_url=image_url,
                       title_url=title_url,
                       company=company
                       )

            yield item