import urllib

import scrapy


class AmericanCharacterSpider(scrapy.Spider):
    # 美国政府雇员
    name = "categories_named_after_politicians"
    allowed_domains = ['en.wikipedia.org']
    # english version
    start_urls = ['https://{}/wiki/Category:Wikipedia_categories_named_after_politicians'.format(allowed_domains[0])]
    # scrapy默认启动的用于处理start_urls的方法
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
            if 'Category' in cl:
                new_category_urls.append(urllib.parse.urljoin('https://{}'.format(self.allowed_domains[0]), cl))
        self.logger.info('parse new_category_urls is %s', new_category_urls)
        # 处理完分类页面后，将所有可能的内容请求链接直接提交处理队列处理
        for url in new_category_urls:
            yield scrapy.Request(url, callback=self.parse_category, meta={'proxy': 'http://192.168.250.1:7897'})

    def parse_category(self, response):
        self.logger.info('parse response is {}, response.url {}'.format(response, response.url))
        search = response.xpath("//main[@id='content']")
        content_urls = search.xpath("//div[@class='mw-category mw-category-columns']//ul/li/a/@href").extract()
        new_categorys = search.xpath("//div[@class='CategoryTreeItem']//a/@href").extract()
        new_content_url = []

        for cl in content_urls:
            if 'Category' not in cl and 'Template' not in cl:
                new_content_url.append(urllib.parse.urljoin('https://{}'.format(self.allowed_domains[0]), cl))
        content_url = new_content_url
        self.logger.info('parse new_content_url is %s', new_content_url)
        for url in content_url:
            yield scrapy.Request(url, callback=self.parse_content, meta={'proxy': 'http://192.168.250.1:7897'})
        for cl in new_categorys:
            if 'Category' in cl:
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
        self.current_url = response.url
        search = response.xpath("//main[@id='content']")
        content_entity = search.xpath("//h1[@id='firstHeading']/span/text()").extract_first()
        content_page_tag_p = search.xpath("//main[@id='content']").xpath(
            "//div[@id='bodyContent']//div[@id='mw-content-text']//div[@class='mw-content-ltr mw-parser-output']/p")
        content_page_list = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        # content_page = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        categories = search.xpath("//div[@id='catlinks']//ul//a/text()").extract()
        # categories = clean_categories(categories)

        counselor_item['content_entity'] = content_entity
        counselor_item['category'] = ';'.join(categories[:10])
        counselor_item['url'] = self.current_url
        counselor_item['content'] = ''.join(content_page_list)
        return counselor_item
