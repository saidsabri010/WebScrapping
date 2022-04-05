import scrapy
from ..items import WhiskyscraperItem


class WhiskySpider(scrapy.Spider):
    name = 'whisky'

    start_urls = ['https://kamernet.nl/huren/kamers-nederland']

    def parse(self, response):
        # title = response.css('.truncate::text').extract()
        # urls = response.css('div.tile-data a').xpath('@href').extract()
        rooms = response.css('div.tile-data')
        items = WhiskyscraperItem()
        for room in rooms:
            url = room.css('a').xpath('@href').extract()
            city = room.css('.tile-city::text').extract()
            roomType = room.css('.tile-room-type::text').extract()
            rentPrice = room.css('.tile-rent::text').extract()
            surfaceSize = room.css('.tile-surface::text').extract()

            items['url'] = url
            items['city'] = city
            items['roomType'] = roomType
            items['rentPrice'] = rentPrice
            items['surfaceSize'] = surfaceSize

            yield items

            """yield {
                'urls': url,
                'city': city,
                'roomType': roomType,
                'rentPrice': rentPrice,
                'surface': surfaceSize
            }"""
        # next_page = response.xpath("//li[@class='next waves-effect']/i/uid/text()").extract_first()
