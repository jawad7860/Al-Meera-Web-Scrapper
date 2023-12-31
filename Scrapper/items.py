# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AlmeeraItem(scrapy.Item):
    CategoryTitle = scrapy.Field()
    Subcategories = scrapy.Field()

class ProductItem(scrapy.Item):
    ItemTitle = scrapy.Field()
    ItemImageURL = scrapy.Field()
    ItemPrice = scrapy.Field()
    ItemBarcode = scrapy.Field()


class SubcategoryItem(scrapy.Item):
    CategoryTitle = scrapy.Field()
    SubcategoryTitle = scrapy.Field()
    Products = scrapy.Field()
    


