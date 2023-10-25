'''
class AlmeeraSpider(scrapy.Spider):
    name = "almeera_spider"
    start_urls = ["https://almeera.online/"]
    Data =[]
    Sub_Data ={}
    prev_response = None
    check = True
    def parse(self, response):
        
        itr = 1  # Initialize the iterator for categories

        download_directory = '.\Images'

        # the directory if it doesn't exist
        os.makedirs(download_directory, exist_ok=True)

        while True:
            # A dynamic CSS selector for categories
            category_selector = f'ul.flyout-menu:nth-child(1) > li:nth-child({itr}) > a:nth-child(1) > span:nth-child(1)::text'
            categories = response.css(category_selector).getall()
            if not categories:
                break  # Break the loop if categories is empty

            #for category in categories:
             #   print(f'Category: {category.strip()}')

            category_data = {

                "CategoryTitle": categories[0].strip(),
                "Subcategories": []
            }

            self.Sub_Data = {}

            # a dynamic CSS selector for subcategories
            
            itr2 = 1
            while True:
                subcategory_selector = f'ul.flyout-menu:nth-child(1) > li:nth-child({itr}) > ul:nth-child(2) > li:nth-child({itr2}) > a:nth-child(1) > span:nth-child(1)::text'
                subcategories = response.css(subcategory_selector).getall()
                subcategory_selector = f'ul.flyout-menu:nth-child(1) > li:nth-child({itr}) > ul:nth-child(2) > li:nth-child({itr2}) > a:nth-child(1)::attr(href)'
                subcategory_href = response.css(subcategory_selector).get()
                if not subcategories:
                    break  # Break the loop if subcategories is empty

                #for subcategory in subcategories:
                #    print(f'Subcategory: {subcategory.strip()}')
                #print(f'Subcategory Href: {subcategory_href}')

                subcategory_data = {
                    "SubcategoryTitle": subcategories[0].strip(),
                    "Products": []
                }

                
                subcategory_url = urljoin(response.url, subcategory_href)
                P_D=yield scrapy.Request(url=subcategory_url, callback=self.parse_subcategory, cb_kwargs={'subcategory_data': subcategory_data})
                subcategory_data["Products"].append(P_D)
                
                
                Nextpage = subcategory_url+ "?pageId=2"
                P_D=yield scrapy.Request(url=Nextpage, callback=self.parse_subcategory, cb_kwargs={'subcategory_data': subcategory_data})
                subcategory_data["Products"].append(P_D)
                print(subcategory_data)
                category_data["Subcategories"].append(subcategory_data)
                itr2 += 1  # Increment the iterator for the next subcategory
                break
            self.Data.append(category_data)
            itr += 1  # Increment the iterator for the next category
            break

        json_data = json.dumps(self.Data, indent=4)
        with open('scraped_data.json', 'w') as json_file:
            json_file.write(json_data)

    def parse_subcategory(self, response,subcategory_data):

        #if self.prev_response and response and response.body == self.prev_response.body:
        #    pass
        #else:

            
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

                product_data = {

                        "ItemTitle": img_alt,
                        "ItemImageURL": img_srcset,
                        "ItemPrice": price,
                   
                    }

                return product_data 



        #self.prev_response =response

'''
import json

# Load your existing JSON data
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

for i in data:
    print(i)
    break