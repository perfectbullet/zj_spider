import os
import time

import numpy as np
import scrapy

from loguru import logger

class Queue:
    candidates = []  # 保存候选的请求列表
    has_viewed = []  # 保存已经被处理过的请求
    save_every = 100  # has_viewed每100次执行一次保存
    # 初始化时需要添加若干个入口请求
    candidates.append('https://zh.wikipedia.org/wiki/Category:%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BC%96%E7%A8%8B')

    # def load_npy(self):  # 用于加载保存在本地的已爬取请求队列
    #     if os.path.exists('has_viewed.npy'):
    #         self.has_viewed = np.load('has_viewed.npy').tolist()
    #
    # def save_has_viewed(self):  # 保存已经访问过的请求队列
    #     np.save('has_viewed.npy', self.has_viewed)

    def add_candidate(self, url):
        # 注意，执行该函数说明获得了一个新的请求，需要待处理（从分类或内容页面解析得到的链接）
        if url not in self.candidates and url not in self.has_viewed:
            self.candidates.append(url)

    def add_candidates(self, url_list):
        # 批量添加注意，执行该函数说明获得了一个新的请求，需要待处理（从分类或内容页面解析得到的链接）
        for url in url_list:
            self.add_candidate(url)

    def delete_candidate(self, url):
        # 注意，执行该函数时，说明有进程已经收到该请求，在处理前需要将候选列表中该请求删除，表示已有进程已经拿到该请求
        if url in self.candidates:
            self.candidates.remove(url)

    def add_has_viewed(self, url):
        # 注意，执行该函数时，说明有进程已经收到请求，并进行了相关处理，现需要更新队列状态
        if url not in self.candidates and url not in self.has_viewed:
            # 如果当前请求既不在候选列表，也不在已爬列表，则加入
            self.has_viewed.append(url)
        elif url in self.candidates and url not in self.has_viewed:
            # 如果当前请求在候选列表中，且不在已爬列表，则说明有进程提前读取该页面，但候选列表还没更新，则加入
            # 并将候选列表对应的请求删除
            self.has_viewed.append(url)
            self.delete_candidate(url)
        elif url in self.candidates and url in self.has_viewed:
            # 如果当前请求在候选列表中，也在已爬列表中，则说明有进程已经完成了爬取，但候选列表没更新，则直接
            # 删掉候选列表中指定的请求
            self.delete_candidate(url)
            # 最后一种情况是当前请求不在候选列表，但在已爬列表，而还能遇到该请求，说明该请求属于滞后请求，无视即可


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
    urlQueue = Queue()
    name = "american_characters"
    allowed_domains = ['zh.wikipedia.org']
    start_urls = ['https://zh.wikipedia.org/wiki/Category:%E6%99%82%E4%BB%A3%E5%B9%B4%E5%BA%A6%E9%A2%A8%E9%9B%B2%E4%BA%BA%E7%89%A9']

    # scrapy默认启动的用于处理start_urls的方法
    def parse(self, response):
        '''
        在维基百科中，页面有两种类型，分别是分类页面，链接中包含Category，否则是百科页面，例如：
        分类页面：https://zh.wikipedia.org/wiki/Category:计算机科学
        百科页面：https://zh.wikipedia.org/wiki/计算机科学
        本方法用于对请求的链接进行处理，如果是分类型的请求，则交给函数1处理，否则交给函数2处理
        :param response: 候选列表中的某个请求
        :return:
        '''
        # 获得一个新请求
        this_url = response.url
        # 说明该请求时一个分类
        logger.info('this_url = {}', this_url)
        if 'Category:' in this_url:
            yield scrapy.Request(this_url, callback=self.parse_category, dont_filter=True)
        else:
            yield scrapy.Request(this_url, callback=self.parse_content, dont_filter=True)

    def parse_category(self, response):
        '''
        处理分类页面的请求
        :param response:
        :return:
        '''
        this_url = response.url
        logger.debug('this_url {}', this_url)
        self.urlQueue.delete_candidate(this_url)
        search = response.xpath("//main[@id='content']")
        category_entity = search.xpath("//h1[@id='firstHeading']/span[3]/text()").extract_first()
        candidate_lists_ = search.xpath("//div[@class='mw-category-generated']//a/@href").extract()
        candidate_lists = []
        # 百科页面有许多超链接是锚链接，需要过滤掉
        for url in candidate_lists_:
            if filter(url):  # 分类请求中过滤掉一些不符合的请求（例如明显包含游戏的关键词都不要爬取）
                continue
            if '/wiki' in url and 'https://zh.wikipedia.org' not in url:
                if ':' not in url or (':' in url and 'Category:' in url):
                    candidate_lists.append('https://zh.wikipedia.org' + url)
        cates_url, content_url = split(candidate_lists)
        self.urlQueue.add_has_viewed(this_url)
        self.urlQueue.add_candidates(content_url)
        self.urlQueue.add_candidates(cates_url)
        logger.info('候选请求数={}', len(self.urlQueue.candidates))
        logger.info('已处理请求数={}', len(self.urlQueue.has_viewed))
        # 处理完分类页面后，将所有可能的内容请求链接直接提交处理队列处理
        if len(self.urlQueue.candidates) == 0:
            self.crawler.engine.close_spider(self)
        for url in self.urlQueue.candidates:
            if url in self.urlQueue.has_viewed:
                continue
            if 'Category:' in url:
                yield scrapy.Request(url, callback=self.parse_category, dont_filter=True)
            else:
                yield scrapy.Request(url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        '''
        处理百科页面请求
        :param response:
        :return:
        '''
        counselor_item = {
            'counselor_item': []
        }
        this_url = response.url
        self.current_url = response.url
        self.urlQueue.delete_candidate(this_url)
        search = response.xpath("//main[@id='content']")
        content_entity = search.xpath("//h1[@id='firstHeading']/span/text()").extract_first()
        content_page_tag_p = search.xpath("//main[@id='content']").xpath("//div[@id='bodyContent']//div[@id='mw-content-text']//div[@class='mw-content-ltr mw-parser-output']/p")
        content_page_list = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        # content_page = content_page_tag_p.xpath('text()|a/text()|b/text()|span/text()').extract()
        categories = search.xpath("//div[@id='catlinks']//ul//a/text()").extract()
        self.urlQueue.add_has_viewed(this_url)
        logger.info('候选请求数={}', len(self.urlQueue.candidates))
        logger.info('已处理请求数={}', len(self.urlQueue.has_viewed))
        # 将当前页面的信息保存下来
        # 如果当前的content的标题或分类属于需要过滤的词（例如我们不想爬取跟游戏有关的，所以包含游戏的请求或分类都不保存）
        is_url_filter = filter(content_entity)
        categories = clean_categories(categories)

        if not is_url_filter:
            counselor_item['content_entity'] = content_entity.replace(':Category', '')
            counselor_item['category'] = ';'.join(categories)
            counselor_item['url'] = this_url
            counselor_item['content'] = ''.format(content_page_list)
            counselor_item['content_page_list'] = ''.format(content_page_list)
            return counselor_item
