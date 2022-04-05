# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WhiskyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    city = scrapy.Field()
    roomType = scrapy.Field()
    rentPrice = scrapy.Field()
    surfaceSize = scrapy.Field()
    pass
