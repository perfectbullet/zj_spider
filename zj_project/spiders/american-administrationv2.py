import urllib

import scrapy


def clean_categories(categories):
    # 过滤掉无关的词
    filter_list = ['维基数据', '维基百科条目', '错误的页面', '失效链接的条目', '条目有永久失效的外部链接',
                   'CS1英语来源', '含有連結內容需訂閱查看的頁面', '使用ISBN魔术链接的页面', '翻譯的條目',
                   '含有英語的條目', '本地相关图片', '与维基数据相同', '不匹配的页面', '包含FAST标识符的维基百科条目',
                   '包含ISNI标识符的维基百科条目', '包含VIAF标识符的维基百科条目',
                   '包含WorldCat实体标识符的维基百科条目', '包含BIBSYS标识符的维基百科条目',
                   '包含BNE标识符的维基百科条目', '包含BNF标识符的维基百科条目', '包含BNFdata标识符的维基百科条目',
                   '包含CANTICN标识符的维基百科条目', '包含GND标识符的维基百科条目', '包含ICCU标识符的维基百科条目',
                   '包含J9U标识符的维基百科条目', '包含KBR标识符的维基百科条目', '包含LCCN标识符的维基百科条目',
                   '包含Libris标识符的维基百科条目', '包含LNB标识符的维基百科条目', '包含NDL标识符的维基百科条目',
                   '包含NKC标识符的维基百科条目', '包含NLA标识符的维基百科条目', '包含NLK标识符的维基百科条目',
                   '包含NSK标识符的维基百科条目', '包含NTA标识符的维基百科条目', '包含PLWABN标识符的维基百科条目',
                   '包含PortugalA标识符的维基百科条目', '包含CINII标识符的维基百科条目',
                   '包含Grammy标识符的维基百科条目', '包含MusicBrainz标识符的维基百科条目',
                   '包含ULAN标识符的维基百科条目', '包含Deutsche Synchronkartei标识符的维基百科条目',
                   '包含DTBIO标识符的维基百科条目', '包含Trove标识符的维基百科条目', '包含CONOR标识符的维基百科条目',
                   '包含NARA标识符的维基百科条目', '包含SNAC-ID标识符的维基百科条目', '包含SUDOC标识符的维基百科条目',
                   '标识符的维基百科条目']
    new_categories = []
    for cs in categories:
        is_ok_category = True
        for tag in filter_list:
            if tag in cs:
                is_ok_category = False
                break
        if is_ok_category:
            new_categories.append(cs)
    return new_categories


class AmericanCharacterSpider(scrapy.Spider):
    # 美国政府雇员
    name = "american-administrationv2"
    allowed_domains = ['zh.wikipedia.org']
    # start_urls = [
    #     'https://zh.wikipedia.org/wiki/Category:%E5%94%90%E7%B4%8D%C2%B7%E5%B7%9D%E6%99%AE%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%93%A1',
    #     'https://zh.wikipedia.org/wiki/Category:%E5%96%AC%C2%B7%E6%8B%9C%E7%99%BB%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%93%A1',
    #     'https://zh.wikipedia.org/wiki/Category:%E5%B0%8F%E5%B8%83%E4%BB%80%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%91%98',
    #     'https://zh.wikipedia.org/wiki/Category:%E5%BE%B7%E6%80%80%E7%89%B9%C2%B7%E8%89%BE%E6%A3%AE%E8%B1%AA%E5%A8%81%E5%B0%94%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%91%98',
    #     'https://zh.wikipedia.org/wiki/Category:%E6%9E%97%E7%99%BB%C2%B7%E7%BA%A6%E7%BF%B0%E9%80%8A%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%91%98',
    #     'https://zh.wikipedia.org/wiki/Category:%E6%AF%94%E5%B0%94%C2%B7%E5%85%8B%E6%9E%97%E9%A1%BF%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%91%98',
    #     'https://zh.wikipedia.org/wiki/Category:%E7%90%86%E6%9F%A5%E5%BE%B7%C2%B7%E5%B0%BC%E5%85%8B%E6%9D%BE%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%91%98',
    #     'https://zh.wikipedia.org/wiki/Category:%E8%B4%9D%E6%8B%89%E5%85%8B%C2%B7%E5%A5%A5%E5%B7%B4%E9%A9%AC%E6%94%BF%E5%BA%9C%E4%BA%BA%E5%91%98'
    # ]
    start_urls = ['https://zh.wikipedia.org/wiki/Category:%E7%BE%8E%E5%9C%8B%E5%90%84%E7%B8%BD%E7%B5%B1%E4%BB%BB%E6%9C%9F%E5%85%A7%E9%96%A3%E6%88%90%E5%93%A1']

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
                new_category_urls.append(urllib.parse.urljoin('https://zh.wikipedia.org', cl))
        self.logger.info('parse new_category_urls is %s', new_category_urls)
        # 处理完分类页面后，将所有可能的内容请求链接直接提交处理队列处理
        for url in new_category_urls:
            yield scrapy.Request(url, callback=self.parse_category, meta={'proxy': 'http://192.168.250.1:7897'})

    def parse_category(self, response):
        self.logger.info('parse response is {}, response.url {}'.format(response, response.url))
        search = response.xpath("//main[@id='content']")
        content_urls = search.xpath("//div[@class='mw-category mw-category-columns']//ul/li/a/@href").extract()
        new_content_url = []

        for cl in content_urls:
            if 'Category' not in cl and 'Template' not in cl:
                new_content_url.append(urllib.parse.urljoin('https://zh.wikipedia.org', cl))
        content_url = new_content_url
        self.logger.info('parse new_content_url is %s', new_content_url)
        for url in content_url:
            yield scrapy.Request(url, callback=self.parse_content, meta={'proxy': 'http://192.168.250.1:7897'})

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
        # 将当前页面的信息保存下来
        # 如果当前的content的标题或分类属于需要过滤的词（例如我们不想爬取跟游戏有关的，所以包含游戏的请求或分类都不保存）
        categories = clean_categories(categories)

        counselor_item['content_entity'] = content_entity
        counselor_item['category'] = ';'.join(categories[:10])
        counselor_item['url'] = self.current_url
        counselor_item['content'] = ''.join(content_page_list)
        return counselor_item
