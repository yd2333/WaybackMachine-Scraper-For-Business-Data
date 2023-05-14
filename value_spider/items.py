# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ValueSpiderItem(scrapy.Item):
    tag = scrapy.Field()
    content = scrapy.Field()
    gvkey= scrapy.Field()
    year= scrapy.Field()
    url = scrapy.Field()

    # def to_dict(self):
    #     return {
    #         "gvkey" : self.gvkey,
    #         "year" : self.year,
    #         "content" : self.content
    #     }