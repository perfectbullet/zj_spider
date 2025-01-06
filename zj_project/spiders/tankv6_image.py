import scrapy


class TankSpider(scrapy.Spider):
    name = "tankv6_image"
    allowed_domains = ["www.bing.com"]
    start_urls = ["https://www.bing.com/images/search?q=M1+Abrams&form=HDRSC2&first=1"]

    def parse(self, response):
        self.current_url = response.url
        item = {
            'title': '',
            'image_urls': '',
        }
        item["title"] = response.xpath('//*[@id="mmComponent_images_1"]/ul')


        yield item
