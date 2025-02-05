import re
import urllib

import scrapy


class MySpider(scrapy.Spider):
    # aircraft_carriers
    name = "List_of_minerals"
    allowed_domains = ['en.wikipedia.org']
    # english version
    start_urls = [
        'https://{}/wiki/List_of_minerals'.format(allowed_domains[0]),
    ]
    # scrapy 默认启动的用于处理start_urls的方法

    def parse(self, response):
        '''
        处理分类页面的请求
        :param response:
        :return:
        '''
        self.logger.info('parse response is {}, response.url {}'.format(response, response.url))
        search = response.xpath("//main[@id='content']")
        item_urls = search.xpath("//div[@class='mw-body-content']//div[@class='mw-content-ltr mw-parser-output']//ul/li/a/@href").extract()
        for url in item_urls:
            if url.startswith('/wiki'):
                complete_url = urllib.parse.urljoin('https://{}'.format(self.allowed_domains[0]), url)
                yield scrapy.Request(complete_url, callback=self.parse_content, meta={'proxy': 'http://192.168.250.1:7897'})

    def parse_content(self, response):
        '''
        处理百科页面请求
        :param response:
        :return:
        '''
        out_item = {
            'image_urls': []
        }
        current_url = response.url
        self.current_url = current_url
        search = response.xpath("//main[@id='content']")
        title = search.xpath("//span[@class='mw-page-title-main']/text()").extract_first()
        content_entity = ' '.join(search.xpath("//h1[@id='firstHeading']").xpath('text()|i/text()').extract())
        content_page_tag_p = search.xpath("//main[@id='content']").xpath(
            "//div[@id='bodyContent']//div[@id='mw-content-text']//div[@class='mw-content-ltr mw-parser-output']/p")
        content_page_list = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        # content_page = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        categories = search.xpath("//div[@id='catlinks']//ul//a/text()").extract()
        # categories = clean_categories(categories)
        image_urls = []
        for u in search.xpath("//a[@class='mw-file-description']/img/@src").extract():
            if u.endswith('.jpg'):
                # 使用sub函数替换匹配的部分为空字符串
                new_u = re.sub(r'thumb/|/\d+px-.+', '', u)
                image_urls.append(new_u)

        new_image_urls = ['https:{}'.format(u) for u in image_urls]

        out_item['title'] = title
        out_item['image_urls'] = new_image_urls
        out_item['content_entity'] = content_entity
        out_item['category'] = ';'.join(categories[:10])
        out_item['url'] = self.current_url
        out_item['content'] = ''.join(content_page_list)
        return out_item
