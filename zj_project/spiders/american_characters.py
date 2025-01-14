import urllib

import scrapy


def split(url_list):
    '''
    分离两种不同的请求类型（分类/内容）
    :return:
    '''
    cates_url, content_url = [], []
    for url in url_list:
        if 'Category:' in url:
            cates_url.append(url)
        else:
            content_url.append(url)
    return cates_url, content_url


def filter(url):
    # 如果字符串url中包含要过滤的词，则为True
    filter_url = ['游戏', '维基',   '幻想', '我的世界', '魔兽']
    for i in filter_url:
        if i in url:
            return True
    return False


def clean_categories(categories):
    # 过滤掉无关的词
    filter_list = ['维基数据', '维基百科条目', '错误的页面', '失效链接的条目', '条目有永久失效的外部链接', 'CS1英语来源', '含有連結內容需訂閱查看的頁面', '使用ISBN魔术链接的页面', '翻譯的條目', '含有英語的條目', '本地相关图片', '与维基数据相同', '不匹配的页面',  '包含FAST标识符的维基百科条目', '包含ISNI标识符的维基百科条目', '包含VIAF标识符的维基百科条目', '包含WorldCat实体标识符的维基百科条目', '包含BIBSYS标识符的维基百科条目', '包含BNE标识符的维基百科条目', '包含BNF标识符的维基百科条目', '包含BNFdata标识符的维基百科条目', '包含CANTICN标识符的维基百科条目', '包含GND标识符的维基百科条目', '包含ICCU标识符的维基百科条目', '包含J9U标识符的维基百科条目', '包含KBR标识符的维基百科条目', '包含LCCN标识符的维基百科条目', '包含Libris标识符的维基百科条目', '包含LNB标识符的维基百科条目', '包含NDL标识符的维基百科条目', '包含NKC标识符的维基百科条目', '包含NLA标识符的维基百科条目', '包含NLK标识符的维基百科条目', '包含NSK标识符的维基百科条目', '包含NTA标识符的维基百科条目', '包含PLWABN标识符的维基百科条目', '包含PortugalA标识符的维基百科条目', '包含CINII标识符的维基百科条目', '包含Grammy标识符的维基百科条目', '包含MusicBrainz标识符的维基百科条目', '包含ULAN标识符的维基百科条目', '包含Deutsche Synchronkartei标识符的维基百科条目', '包含DTBIO标识符的维基百科条目', '包含Trove标识符的维基百科条目', '包含CONOR标识符的维基百科条目', '包含NARA标识符的维基百科条目', '包含SNAC-ID标识符的维基百科条目', '包含SUDOC标识符的维基百科条目', '标识符的维基百科条目']
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
    name = "american_characters"
    allowed_domains = ['zh.wikipedia.org']
    start_urls = ['https://zh.wikipedia.org/wiki/Category:%E6%99%82%E4%BB%A3%E5%B9%B4%E5%BA%A6%E9%A2%A8%E9%9B%B2%E4%BA%BA%E7%89%A9']

    # scrapy默认启动的用于处理start_urls的方法
    def parse(self, response):
        '''
        处理分类页面的请求
        :param response:
        :return:
        '''
        self.logger.info('parse response is {}, response.url {}', response, response.url)
        search = response.xpath("//main[@id='content']")
        content_url = search.xpath("//div[@class='mw-category mw-category-columns']//ul/li/a/@href").extract()
        new_content_url = []

        for cl in content_url:
            if 'Category' not in cl and 'Template' not in cl:
                new_content_url.append(urllib.parse.urljoin('https://zh.wikipedia.org', cl))
        content_url = new_content_url
        self.logger.info('parse new_content_url is {}', new_content_url)
        # 处理完分类页面后，将所有可能的内容请求链接直接提交处理队列处理
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
        content_page_tag_p = search.xpath("//main[@id='content']").xpath("//div[@id='bodyContent']//div[@id='mw-content-text']//div[@class='mw-content-ltr mw-parser-output']/p")
        content_page_list = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        # content_page = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        categories = search.xpath("//div[@id='catlinks']//ul//a/text()").extract()
        # 将当前页面的信息保存下来
        # 如果当前的content的标题或分类属于需要过滤的词（例如我们不想爬取跟游戏有关的，所以包含游戏的请求或分类都不保存）
        categories = clean_categories(categories)

        counselor_item['content_entity'] = content_entity.replace(':Category', '')
        counselor_item['category'] = ';'.join(categories)
        counselor_item['url'] = self.current_url
        counselor_item['content'] = ''.join(content_page_list)
        return counselor_item
