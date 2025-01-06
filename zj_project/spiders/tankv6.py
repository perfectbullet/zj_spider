import scrapy


class TankSpider(scrapy.Spider):
    name = "tankv6"
    allowed_domains = ["www.militaryfactory.com"]
    start_urls = ["https://www.militaryfactory.com/armor/detail.php?armor_id={}".format(i) for i in range(1, 1000, 1)]
    start_urls = ["https://www.militaryfactory.com/armor/detail.php?armor_id=3", ]

    def parse(self, response):
        self.current_url = response.url
        item = {}
        item["title"] = response.xpath('/html/body/div[5]/div[1]/div[1]/h1/span/text()').extract_first()
        country_and_year = response.xpath('/html/body/div[5]/div/div[1]/h3/text()').extract_first().split('|')
        item['country'] = country_and_year[0]
        item['year'] = country_and_year[1]
        item['image_url'] = 'https://www.militaryfactory.com' + response.xpath(
            '/html/body/div[5]/div/div[2]/a/div/img[2]/@src').extract_first()
        item['image_urls'] = [item['image_url'], ]
        item['content'] = ''
        mySlides_fades = response.xpath('//div[@class="slideshow-container"]/div')
        for fade in mySlides_fades:
            fade_image = fade.xpath('./img/@src').extract_first()
            fade_image = '{}{}{}'.format('https://', self.allowed_domains[0], fade_image)
            item['image_urls'].append(fade_image)
        for span in response.xpath('/html/body/div[6]/div/span/text()'):
            text = span.extract()
            if text == '\r\n':
                text = ''
            item['content'] = item['content'] + text
        for span in response.xpath('/html/body/div[8]/div/span/text()'):
            text = span.extract()
            if text == '\r\n':
                text = ''
            item['content'] = item['content'] + text

        item['detail_image_urls'] = []
        for img_div in response.xpath('/html/body/div[15]/div/div/div/div'):
            img_url = 'www.militaryfactory.com' + img_div.xpath('//div[1]/img[2]/@src').extract_first()
            item['detail_image_urls'].append(img_url)
            print(item['detail_image_urls'])

        performence_and_power_overview = response.xpath(
            '/html/body/div[9]/div/div[2]/div[1]/span[1]/text()').extract_first()
        div_performence = response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor2"][1]')
        try:
            speedm = div_performence.xpath('//div[1]/div[2]/div[2]/span[1]/text()').extract_first()
            speedk = div_performence.xpath('//div[1]/div[2]/div[2]/span[2]/text()').extract_first()
            rangem = div_performence.xpath('//div[1]/div[2]/div[3]/span[1]/text()').extract_first()
            rangek = div_performence.xpath('//div[1]/div[2]/div[3]/span[2]/text()').extract_first()
        except:
            pass
        item['performence_and_power'] = {
            'overview': performence_and_power_overview,
            'road_speed': speedm + '||' + speedk,
            'range': rangem + '||' + rangek,
        }
        structure_overview = response.xpath('/html/body/div[11]/div/div[1]/span[2]/text()').extract_first()
        structure_1 = ''
        for s in response.xpath('/html/body/div[11]/div/div[2]/div[1]/span/text()'):
            structure_1 = structure_1 + '||' + s.extract()

        structure_2 = '||'.join(
            [s.extract() for s in response.xpath('/html/body/div[11]/div/div[2]/div[2]/span/text()')])
        structure_3 = '||'.join(
            [s.extract() for s in response.xpath('/html/body/div[11]/div/div[2]/div[3]/span/text()')])
        structure_4 = '||'.join(
            [s.extract() for s in response.xpath('/html/body/div[11]/div/div[2]/div[4]/span/text()')])
        structure_5 = '||'.join(
            [s.extract() for s in response.xpath('/html/body/div[11]/div/div[2]/div[5]/span/text()')])

        item['structure'] = {
            'overview': structure_overview,
            'crew': structure_1,
            'length': structure_2,
            'windth': structure_3,
            'Height': structure_4,
            'weight': structure_5

        }
        Armament_overview = response.xpath('/html/body/div[12]/div/div[1]/span[2]/text()').extract_first()
        Armament1 = '||'.join([s.extract() for s in response.xpath('/html/body/div[12]/div/div[2]/div[1]/span/text()')])
        Armament2 = '||'.join([s.extract() for s in response.xpath('/html/body/div[12]/div/div[2]/div[2]/span/text()')])
        Armament3 = '||'.join([s.extract() for s in response.xpath('/html/body/div[12]/div/div[2]/div[3]/span/text()')])

        item['Armament'] = {
            'overview': Armament_overview,
            'Armament1': Armament1,
            'Armament2': Armament2,
            'Armament2': Armament3
        }
        variants_overview = response.xpath('/html/body/div[12]/div/div[1]/span[2]/text()').extract_first()
        variants1 = '||'.join([s.extract() for s in response.xpath('/html/body/div[12]/div/div[2]/div/span/text()')])
        print(response.url + "variants", variants1)
        item['Variants'] = {
            'overview': variants_overview,
            'variants': variants1
        }

        yield item
