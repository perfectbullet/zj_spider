import scrapy


class YiliaoqixieSpider(scrapy.Spider):
    name = "yiliaoqixiev3"
    allowed_domains = ["https://www.3618med.com"]
    start_urls = ["https://www.3618med.com/product/p{}.html".format(i) for i in range(1, 4800, 1)]
    current_url = ''

    def parse(self, response):
        self.current_url = response.url
        divlivst = response.xpath('//ul[@class="tia_l_list"]/li')
        for idx, li in enumerate(divlivst, start=1):
            print('idx is {}'.format(idx))
            title = li.xpath('./span[2]/a/h2/text()').extract_first().strip()
            title_url = li.xpath('./span[@class="w2"]/a//@href').extract_first()
            image_url = li.xpath('./span[@class="w1"]/a/img//@src').extract_first()
            date = li.xpath('./span[2]/p[2]/text()').extract_first().strip()
            a_ls = li.xpath('./span[2]/p[3]/a')
            ml = ''
            for b in a_ls:
                one_text = b.xpath('./text()').extract_first().strip()
                ml = ml + '->' + one_text

            item = dict(title=title,
                        title_url=title_url,
                        image_url=image_url,
                        date=date,
                        ml=ml
                        )
            yield item
