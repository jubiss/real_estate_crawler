# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PropertyItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    rooms = scrapy.Field()
    bathrooms = scrapy.Field()
    garages = scrapy.Field()
    rent = scrapy.Field()
    amenities = scrapy.Field()
    images = scrapy.Field()
    condominio = scrapy.Field()
    link = scrapy.Field()
    scraping_date = scrapy.Field()
    scraped_site = scrapy.Field()