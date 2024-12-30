import scrapy

from zj_project.items import AirlineItemv3


class ArmorsZj(scrapy.Spider):
    name = "ArmorsZj"
    current_url = ""
    allowed_domains = ["cn.bing.com"]
    start_urls = ["https://cn.bing.com/images/search?q=%E8%A3%85%E7%94%B2%E8%BD%A6%E5%9B%BE%E7%89%87&form=IQFRML&first={}".format(u) for u in range(1, 2)]

    def parse(self, response):
        self.current_url = response.url
        # //	从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置（取子孙节点）。
        # /html/body/div[3]/div[5]/div/div[1]/ul[1]
        divList = response.xpath('//div[@class="dgControl dtl hover"')
        print(len(divList))
        for div in divList:
            # print('{} div {}\n{}\n'.format('*' * 100, '*' * 100, div, ))
            # . 选取当前节点。 <a href="/search?aircraft=25083&amp;display=detail">
            # //*[@id="layout-page"]/div[2]/section/section/section/div/section[2]/div/div[1]/div/div[1]/div[2]/div
            imgLink = div.xpath('./div[1]/div[2]/div[1]/a[1]/img[1]').attrib['src']  # 1.封面图片链接
            name = div.xpath('./div[2]/div[2]/div[1]/div[2]/a/text()').extract_first().strip()  # 1.封面图片链接
            air_force = div.xpath('./div[2]/div[2]/div[1]/div[1]/a/text()').extract_first().strip()  # 1.封面图片链接
            date = div.xpath('./*[@class="ps-v2-results-col ps-v2-results-col-location-date"]/div[2]/div[1]/div[2]/a[2]/text()').extract_first().strip()
            location = div.xpath('./*[@class="ps-v2-results-col ps-v2-results-col-location-date"]/div[2]/div[1]/div[1]/a[1]/text()').extract_first().strip()
            # item = AirlineItemv3(image_urls=[imgLink,], name=name, air_force=air_force, date=date, location=location)
            item = dict(image_urls=[imgLink,], name=name, air_force=air_force, date=date, location=location)
            item['proxy'] = response.meta['proxy']
            yield item
