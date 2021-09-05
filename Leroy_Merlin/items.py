# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def get_price(value):
    try:
        value = int(value.replace('\xa0', '').replace(' ', ''))
    except Exception:
        return value
    return value

class LeroyMerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field()
    characteristic = scrapy.Field()
    value_char = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
