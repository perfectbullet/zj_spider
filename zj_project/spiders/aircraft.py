import scrapy


class AircraftSpider(scrapy.Spider):
    name = "aircraftv1"
    allowed_domains = ["www.militaryfactory.com"]
    start_urls = ["https://www.militaryfactory.com/aircraft/detail.php?aircraft_id={}".format(i) for i in range(1,10000,1)]
    current_url = ''
    def parse(self, response):
        item = {}
        self.current_url = response.url
        item["title"] = response.xpath('/html/body/div[5]/div[1]/div[1]/h1/span/text()').extract_first()
        item["title2"]=response.xpath('/html/body/div[5]/div/div[1]/h2/text()').extract_first()
        country_and_year = response.xpath('/html/body/div[5]/div/div[1]/h3/text()').extract_first().split('|')
        item['country'] = country_and_year[0]
        item['year'] = country_and_year[1]
        item['image_url'] = 'https://www.militaryfactory.com' + response.xpath(
            '/html/body/div[5]/div/div[2]/a/div/img[2]/@src').extract_first()
        item['image_urls'] = [item['image_url']]
        item['content'] = ''
        for span in response.xpath('/html/body/div[6]/div/span/text()'):
            text = span.extract().strip()
            if text == '\t\r\n':
                text = ''
            item['content'] = item['content'] + text
        for span in response.xpath('/html/body/div[7]/div/span/text()'):
            text = span.extract().strip()
            if text == '\r\n':
                text = ''
            item['content'] = item['content']+ text
        item['detail_image_urls'] = []
        for img_div in response.xpath('//div[@class="slideshow-container"]/div'):
            img_url = 'www.militaryfactory.com' + img_div.xpath('./img/@src').extract_first()
            item['detail_image_urls'].append(img_url)
            print(item['detail_image_urls'])
        mySlides_fades = response.xpath('//div[@class="slideshow-container"]/div')
        for fade in mySlides_fades:
                fade_image = fade.xpath('./img/@src').extract_first()
                fade_image = '{}{}{}'.format('https://', self.allowed_domains[0], fade_image)
                item['image_urls'].append(fade_image)
        performence_and_power_overview = response.xpath('/html/body/div[7]/div/div[1]/span[2]/text()').extract_first()
        div_performence = response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor1"]')
        try:
            # yili
            propulsion = div_performence.xpath('//div[2]/div[1]/span[1]/text()').extract_first()
            speedm = div_performence.xpath('//div[2]/div[2]/span[1]/text()').extract_first()
            speedk = div_performence.xpath('//div[2]/div[2]/span[2]/text()').extract_first()
            cspeedm = div_performence.xpath('///div[2]/div[3]/span[1]/text()').extract_first()
            cspeedk = div_performence.xpath('///div[2]/div[3]/span[2]/text()').extract_first()
            # gognlig
            cellingm = div_performence.xpath('//div[2]/div[4]/span[1]/text()').extract_first()
            cellingk = div_performence.xpath('//div[2]/div[4]/span[2]/text()').extract_first()
            rangem = div_performence.xpath('//div[2]/div[5]/span[1]/text()').extract_first()
            rangek = div_performence.xpath('//div[2]/div[5]/span[2]/text()').extract_first()
            climbm = div_performence.xpath('//div[2]/div[6]/span[1]/text()').extract_first()
            climbk = div_performence.xpath('//div[2]/div[6]/span[2]/text()').extract_first()
            print(response.url + ' speed is ',rangek, rangem)
        except:
            pass
        item['performance'] = {
            'overview': performence_and_power_overview,
            'propulsion':propulsion,
            'maxspeed': speedm + '||' + speedk,
            'cruisespeed': cspeedm + '||' + cspeedk,
            'ceiling': cellingm + '||' + cellingk,
            'range' :rangem + '||' + rangek,
            'climb' : climbm + '||' + climbk
        }
        structure_overview = response.xpath('/html/body/div[8]/div/div[1]/span[2]/text()').extract_first()
        structure_1 = ''
        for s in response.xpath('/html/body/div[8]/div/div[2]/div[1]/span/text()'):
            structure_1 = structure_1 + '||' + s.extract()

        performence_2 = '||'.join(
            [s.extract() for s in response.xpath('/html/body/div[8]/div/div[2]/div[2]/span/text()')])
        structure_3 = '||'.join([s.extract() for s in response.xpath('/html/body/div[8]/div/div[2]/div[3]/span/text()')])
        structure_4 = '||'.join([s.extract() for s in response.xpath('/html/body/div[8]/div/div[2]/div[4]/span/text()')])
        structure_5 = '||'.join([s.extract() for s in response.xpath('/html/body/div[8]/div/div[2]/div[5]/span/text()')])
        item['structure'] = {
            'overview': structure_overview,
            'crew': structure_1,
            'length': performence_2,
            'width' : structure_3,
            'height': structure_4,
            'mtow' : structure_5

        }
        armament_overview = response.xpath('/html/body/div[9]/div/div[1]/span[2]/text()').extract_first()
        armament1 = '||'.join(
            [s.extract().strip() for s in response.xpath('/html/body/div[9]/div/div[2]/div[1]/span/text()')])
        print(response.url + "variants", armament1)
        item['armament']={
            'overview' : armament_overview,
            'armament1' : armament1
        }
        variants_overview = response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor2"][2]/div/div[1]/span[2]/text()').extract_first()
        variants1 = '||'.join(
            [s.extract().strip() for s in response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor2"][2]/div/div[2]/div/span/text()')])
        print(response.url + "variants", variants1)
        item['Variants'] = {
            'overview': variants_overview,
            'variants': variants1
        }
        operators_overview = response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor1"][3]/div/div[1]/span[2]/text()[1]').extract_first().strip()
        operator1=response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor1"][3]/div/div[1]/span[2]/span/text()').extract_first()
        l2 = response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor1"][3]/div/div[1]/span[2]/text()[5]').extract_first()
        l1 = response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor1"][3]/div/div[1]/text()[7]').extract_first().strip()

        operator2=response.xpath('/html/body/div[@class="contentStripOuter stripBGcolor1"][3]/div/div[1]/span[3]/text()').extract_first()
        # print(response.url + "variants", variants1)
        item['operators']={
            'overview' : operators_overview ,
            'operators1' : operator1.strip() + l2,
            'operators2' : operator2.strip() + l1
        }

        yield item

