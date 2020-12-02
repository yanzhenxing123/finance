# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    scheme = scrapy.Field()
    created_at = scrapy.Field()
    raw_text = scrapy.Field()
    source = scrapy.Field()
    platform = scrapy.Field()
    insert_time = scrapy.Field()


