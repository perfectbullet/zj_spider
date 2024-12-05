import scrapy

from zj_project.items import AirlineItem


class AirlinesSpider(scrapy.Spider):
    name = "airlines"
    print('spider {}'.format(name))
    allowed_domains = ["www.airliners.net"]
    crawled_cache = '{}_crawled_urls.txt'.format(name)
    start_urls = ["https://www.airliners.net/search?photoCategory=9&page={}".format(u) for u in range(1, 13000)]
    # 去掉爬取过的

    with open(crawled_cache, mode='a+', encoding='utf8') as f:
        readed_urls = {u for u in f.readline()}
        start_urls = list(set(start_urls).difference(readed_urls))

    def parse(self, response):

        # //	从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置（取子孙节点）。
        divList = response.xpath('//div[@class="ps-v2-results-display-detail-col photo even" or @class="ps-v2-results-display-detail-col photo odd"]/div ')
        print(len(divList))
        # print('{}\nlen div list {}\n{}\n'.format('*' * 100, len(divList), '*' * 100))
        for div in divList:
            # print('{} div {}\n{}\n'.format('*' * 100, '*' * 100, div, ))
            # . 选取当前节点。 <a href="/search?aircraft=25083&amp;display=detail">
            # //*[@id="layout-page"]/div[2]/section/section/section/div/section[2]/div/div[1]/div/div[1]/div[2]/div
            imgLink = div.xpath('./div[1]/div[2]/div[1]/a[1]/img[1]').attrib['src']  # 1.封面图片链接
            name = div.xpath('./div[2]/div[2]/div[1]/div[2]/a/text()').extract_first().strip()  # 1.封面图片链接
            air_force = div.xpath('./div[2]/div[2]/div[1]/div[1]/a/text()').extract_first().strip()  # 1.封面图片链接
            date = div.xpath('./*[@class="ps-v2-results-col ps-v2-results-col-location-date"]/div[2]/div[1]/div[2]/a[2]/text()').extract_first().strip()
            location = div.xpath('./*[@class="ps-v2-results-col ps-v2-results-col-location-date"]/div[2]/div[1]/div[1]/a[1]/text()').extract_first().strip()
            item = AirlineItem(image_url=imgLink, name=name, air_force=air_force, date=date, location=location)
            yield item
