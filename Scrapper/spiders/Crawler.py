import scrapy
from urllib.parse import urljoin
import urllib.request
import os

from Scrapper.items import AlmeeraItem, SubcategoryItem, ProductItem



class AlmeeraSpider(scrapy.Spider):
    name = "almeera_spider"
    start_urls = ["https://almeera.online/"]

    def parse(self, response):
        
        itr = 1  # Initialize the iterator for categories


        while True:
            # A dynamic CSS selector for categories
            category_selector = f'ul.flyout-menu:nth-child(1) > li:nth-child({itr}) > a:nth-child(1) > span:nth-child(1)::text'
            categories = response.css(category_selector).getall()
            if not categories:
                break  # Break the loop if categories is empty



       
            almeera_item = AlmeeraItem()
            almeera_item['CategoryTitle'] = categories[0].strip()
            almeera_item['Subcategories'] = []

            

            # a dynamic CSS selector for subcategories
            
            itr2 = 1
            while True:

                subcategory_selector = f'ul.flyout-menu:nth-child(1) > li:nth-child({itr}) > ul:nth-child(2) > li:nth-child({itr2}) > a:nth-child(1) > span:nth-child(1)::text'
                subcategories = response.css(subcategory_selector).getall()
                subcategory_selector = f'ul.flyout-menu:nth-child(1) > li:nth-child({itr}) > ul:nth-child(2) > li:nth-child({itr2}) > a:nth-child(1)::attr(href)'
                subcategory_href = response.css(subcategory_selector).get()
                if not subcategories:
                    break  # Break the loop if subcategories is empty

                subcategory_data=SubcategoryItem()
                subcategory_data['SubcategoryTitle']=subcategories[0].strip()
                subcategory_data['CategoryTitle'] = categories[0].strip()
                subcategory_data['Products'] = []
                subcategory_url = urljoin(response.url, subcategory_href)
                yield scrapy.Request(url=subcategory_url, callback=self.parse_subcategory, cb_kwargs={'subcategory_data': subcategory_data})
                
                
                
                Nextpage = subcategory_url+ "?pageId=2"
                yield scrapy.Request(url=Nextpage, callback=self.parse_subcategory, cb_kwargs={'subcategory_data': subcategory_data})

                almeera_item['Subcategories'].append(subcategory_data)
                itr2 += 1  # Increment the iterator for the next subcategory
            
            
            itr += 1  # Increment the iterator for the next category
            



    def parse_subcategory(self, response,subcategory_data):


            
            for i in range(1,6):

            

                product_selector=f'.products-grid > li:nth-child({i})'
                product_items = response.css(product_selector)
                # Extract product details
                try:
                    img_srcset = product_items.css('div img::attr(srcset)').get().split(" ")[0]
                except:
                    img_srcset = product_items.css('div img::attr(srcset)').get()
                img_alt = product_items.css('div img::attr(alt)').get()
                price = product_items.css('span.price.product-price::text').get()

            

                product_item2 = ProductItem()
                product_item2['ItemTitle'] = img_alt,
                product_item2['ItemImageURL'] = img_srcset
                product_item2['ItemPrice'] = price

                subcategory_data['Products'].append(product_item2)
                yield subcategory_data


