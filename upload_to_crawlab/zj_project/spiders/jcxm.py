import scrapy


class JcxmSpider(scrapy.Spider):
    name = "jcxm"
    allowed_domains = ["www.zytesting.com"]
    start_urls = ["http://www.zytesting.com/jcxm/{}.html".format(i) for i in range(60,300,1)]

    def parse(self, response):
        item = {}
        item['title'] = response.xpath('/html/body/div[4]/div[2]/div/div/div[2]/h2/text()').extract_first()
        image_url1= 'http://www.zytesting.com/'+response.xpath('/html/body/div[4]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/img/@src').extract_first()
        item['neirong']=response.xpath('/html/body/div[4]/div[2]/div/div/div[2]/p/text()').extract_first()
        item['image_urls'] = [image_url1]

        yield  item
