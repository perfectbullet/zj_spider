import scrapy


class ShipsSpider(scrapy.Spider):
    name = "shipsv2"
    allowed_domains = ["junshi.china.com"]
    start_urls = ["https://junshi.china.com/wuqi/so/130002593_0_0_{}.html".format(i) for i in range(1, 40, 1)]

    def parse(self, response):
        item = {}
        class_new_urls_li = response.xpath('//div[@class="search_list"]/ul[@class="mod_pic_3 clearfix"]/li')
        for li in class_new_urls_li:
            item['title'] = li.xpath('./h3/a/text()').extract_first()
            item['image_url'] = li.xpath('./a/img/@src').extract_first()
            # use to  download images
            item['image_urls'] = [item['image_url'],]
            item['title_url'] = li.xpath('./h3/a/@href').extract_first()
            yield scrapy.Request(url=item['title_url'], meta={'item': item}, callback=self.sec_handler)

    def sec_handler(self, response):

        item = response.meta['item']
        # 获取子页面内容
        item['fuyiyu'] = response.xpath('//*[@id="info-flow"]/div[1]/div[3]/p/text()').extract_first()  # 服役单位
        item['wuqizhaungbei'] = response.xpath('//*[@id="info-flow"]/div[3]/div[2]/p/text()').extract_first()  # 武器装备
        item['zhuyaoyonghu'] = response.xpath('//*[@id="info-flow"]/div[4]/div[2]/p/text()').extract_first()  # 主要用户
        item['xinghaoyanbian'] = response.xpath('//*[@id="info-flow"]/div[5]/div[2]/p/text()').extract_first()  # 型号演变
        item['shiyongqingkuang'] = response.xpath('//*[@id="info-flow"]/div[6]/div[2]/p/text()').extract_first()  # 使用情况
        item['jiegoutedian'] = response.xpath('//*[@id="info-flow"]/div[8]/div[2]/p/text()').extract_first()  # 结构特点
        r_tr = response.xpath('//*[@id="info-flow"]/div[1]/ul/li')
        params = ''
        for idx, li in enumerate(r_tr, start=1):
            mingcheng = li.xpath('./em/text()').extract_first()  # 名称
            neirong = li.xpath('./p/text()').extract_first()  # 建造时间
            params += "||" + mingcheng + ":" + neirong
        item['xiangxicanshu'] = {
            'mingcheng': mingcheng,
            'neirong': neirong

        }
        return item
