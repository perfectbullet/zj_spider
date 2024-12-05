import scrapy
from scrapy.http import Request, Response
from zj_project.items import YlqxItem

class YlqxSpider(scrapy.Spider):
    name = "ylqx"
    allowed_domains = ["ylqx.qgyyzs.net"]
    start_urls = ["https://ylqx.qgyyzs.net/zs/list_0_0_0_{}.htm".format(i) for i in range(1, 2754, 1)]
    current_url = ""
    # 去掉爬取过的
    with open('ylqx_crawled_urls.txt', mode='a+', encoding='utf8') as f:
        old_lines = [line.strip() for line in f.readlines()]

        readed_urls = {u for u in f.readline()}
        start_urls = list(set(start_urls).difference(readed_urls))
        if old_lines:
            start_urls.insert(0, old_lines[-1])

    def parse(self, response: Response):
        self.current_url = response.url
        divList = response.xpath('//div[@class="r_list"]')
        for idx, div in enumerate(divList, start=1):
            print('idx is {}'.format(idx))
            # print('{} div {}\n{}\n'.format('*' * 100, '*' * 100, div, ))
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
