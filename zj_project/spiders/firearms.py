import scrapy


class FirearmsSpider(scrapy.Spider):
    name = "firearmsv2"
    allowed_domains = ["www.militaryfactory.com"]
    schema = 'https://'
    start_urls = ["https://www.militaryfactory.com/smallarms/detail.php?smallarms_id={}".format(i) for i in range(1,3000,1)]

    def parse(self, response):
        item = {}
        self.current_url = response.url
        item["title"] = response.xpath('/html/body/div[5]/div[1]/div[1]/h1/span/text()').extract_first()
        country_and_year = response.xpath('/html/body/div[5]/div/div[1]/h3/text()').extract_first().split('|')
        item['country'] = country_and_year[0]
        item['year'] = country_and_year[1]
        item['image_url'] = self.schema + self.allowed_domains[0] + response.xpath('/html/body/div[5]/div/div[2]/a/div/img[2]/@src').extract_first()
        item['image_urls'] = [item['image_url'] ]
        item['content'] = ''
        for span in response.xpath('/html/body/div[6]/div/span/text()'):
            text = span.extract()
            if text == '\r\n':
                text = ''
            item['content'] = item['content'] + text
        for span in response.xpath('/html/body/div[7]/div/span/text()'):
            text = span.extract()
            if text == '\r\n':
                text = ''
            item['content'] = item['content'] + text
        item['detail_image_urls'] = []
        for img_div in response.xpath('/html/body/div[15]/div/div/div/div'):
            img_url = self.schema + self.allowed_domains[0] + img_div.xpath('//div[1]/img[2]/@src').extract_first()
            item['detail_image_urls'].append(img_url)
            print(item['detail_image_urls'])
        performence_and_power_overview = response.xpath('/html/body/div[7]/div/div[1]/span[2]/text()').extract_first()
        div_performence = response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor1"]')
        try:
            # yili
            oalengthm=div_performence.xpath('//div[2]/div[1]/span[1]/text()').extract_first()
            oalengthk=div_performence.xpath('//div[2]/div[1]/span[2]/text()').extract_first()
            lengthm = div_performence.xpath('//div[1]/div[2]/div[2]/span[1]/text()').extract_first()
            # gognlig
            lengthk = div_performence.xpath('//div[1]/div[2]/div[2]/span[2]/text()').extract_first()
            weightm = div_performence.xpath('//div[1]/div[2]/div[3]/span[1]/text()').extract_first()
            weightk = div_performence.xpath('//div[1]/div[2]/div[3]/span[2]/text()').extract_first()
            action=div_performence.xpath('//div[2]/div[4]/span[1]/text()').extract_first()
            print(response.url + ' speed is ', lengthm, weightm)
        except:
            pass
        item['Physical'] = {
            'overview': performence_and_power_overview,
            'OA_length':oalengthm+'||'+oalengthk,
            'Barrel_length': lengthm + '||' + lengthk,
            'range': weightm + '||' + weightk,
            'Action':action
        }
        structure_overview = response.xpath('/html/body/div[8]/div/div[1]/span[2]/text()').extract_first()
        structure_1 = ''
        for s in response.xpath('/html/body/div[8]/div/div[2]/div[1]/span/text()'):
            structure_1 = structure_1 + '||' + s.extract()

        performence_2 = '||'.join([s.extract() for s in response.xpath('/html/body/div[8]/div/div[2]/div[1]/span/text()')])
        # structure_3 = '||'.join([s.extract() for s in response.xpath('/html/body/div[11]/div/div[2]/div[3]/span/text()')])
        # structure_4 = '||'.join([s.extract() for s in response.xpath('/html/body/div[11]/div/div[2]/div[4]/span/text()')])
        # structure_5 = '||'.join([s.extract() for s in response.xpath('/html/body/div[11]/div/div[2]/div[5]/span/text()')])
        item['performance'] = {
            'overview': structure_overview,
            'max.Eff.Range': structure_1,
            'Rate-of-Fire': performence_2,

        }

        variants_overview = response.xpath('/html/body/div[9]/div/div[1]/span[2]/text()').extract_first()
        variants1 = '||'.join([s.extract().strip() for s in response.xpath('/html/body/div[9]/div/div[2]/div/span/text()')])
        print(response.url + "variants", variants1)
        item['Variants'] = {
            'overview': variants_overview,
            'variants': variants1
        }

        yield item

