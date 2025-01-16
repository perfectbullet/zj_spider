import re
import urllib

import scrapy


class AmericanCharacterSpider(scrapy.Spider):
    # aircraft_carriers
    name = "destroyersv2"
    allowed_domains = ['en.wikipedia.org']
    # english version
    start_urls = ['https://{}/wiki/Category:Destroyers'.format(allowed_domains[0])]
    # scrapy 默认启动的用于处理start_urls的方法

    def parse(self, response):
        '''
        处理分类页面的请求
        :param response:
        :return:
        '''
        self.logger.info('parse response is {}, response.url {}'.format(response, response.url))
        search = response.xpath("//main[@id='content']")
        category_urls = search.xpath("//div[@class='mw-category mw-category-columns']//div[@class='CategoryTreeItem']//a/@href").extract()
        new_category_urls = []

        for cl in category_urls:
            if re.search(r'Lists_of_destroyers', cl) is None and re.search(r'Category|Destroyers', cl) is not None:
                new_category_urls.append(urllib.parse.urljoin('https://{}'.format(self.allowed_domains[0]), cl))
        self.logger.info('parse new_category_urls is %s', new_category_urls)
        # 处理完分类页面后，将所有可能的内容请求链接直接提交处理队列处理
        for url in new_category_urls:
            yield scrapy.Request(url, callback=self.parse_category, meta={'proxy': 'http://192.168.250.1:7897'})

    def parse_category(self, response):
        self.logger.info('parse response is {}, response.url {}'.format(response, response.url))
        search = response.xpath("//main[@id='content']")
        content_urls = search.xpath("//div[@class='mw-category mw-category-columns']//ul/li/a/@href").extract()
        content_urlsv2 = search.xpath(
            "//div[@id='bodyContent']//div[@class='mw-category-generated']//div[@class='mw-category-group']//ul//li/a/@href").extract()
        new_categories = search.xpath("//div[@class='CategoryTreeItem']//a/@href").extract()
        new_content_url = []

        for cl in content_urls + content_urlsv2:
            if not re.search(':Category|Template|List_of|Lists_of', cl):
                # 当前分类 carrier
                new_content_url.append(urllib.parse.urljoin('https://{}'.format(self.allowed_domains[0]), cl))
        content_urls = new_content_url

        self.logger.info('parse new_content_url is %s', new_content_url)
        self.logger.info('parse new_categories is %s', new_categories)
        for url in content_urls:
            yield scrapy.Request(url, callback=self.parse_content, meta={'proxy': 'http://192.168.250.1:7897'})
        for cl in new_categories:
            if (re.search('Category', cl) and re.search('Destroyers|Destroyers|destroyers|destroyer', cl)):
                yield scrapy.Request(urllib.parse.urljoin('https://{}'.format(self.allowed_domains[0]), cl), callback=self.parse_category, meta={'proxy': 'http://192.168.250.1:7897'})

    def parse_content(self, response):
        '''
        处理百科页面请求
        :param response:
        :return:
        '''
        counselor_item = {
            'image_urls': []
        }
        current_url = response.url
        self.current_url = current_url
        search = response.xpath("//main[@id='content']")
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
        counselor_item['image_urls'] = new_image_urls
        counselor_item['content_entity'] = content_entity
        counselor_item['category'] = ';'.join(categories[:10])
        counselor_item['url'] = self.current_url
        counselor_item['content'] = ''.join(content_page_list)
        return counselor_item
