import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]


    # ----------- getting single book and their prize ------------------
    def parse_simple(self, response): 
        books = response.css('article.product_pod')  # getting response
        for book in books:
            # yield act as return function
            yield {
                'name': book.css('h3 a::attr(title)').get(),
                'price':book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href'],
            }
        
        next_p = response.css('li.next a ::attr(href)').get()
        
        if next_p is not None:
            if 'catalogue/' in next_p:
                next_p = next_p.split('/')[0] + '/category/books_1/' + next_p.split('/')[1]
                next_p_url = "https://books.toscrape.com/" + next_p
            else: 
                next_p = 'catalogue/category/books_1/' + next_p.split('/')[0]
                next_p_url = "https://books.toscrape.com/" + next_p
            yield response.follow(next_p_url, callback= self.parse)
    
    # ---------------- getting more details -----------------------------
    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in relative_url:
                next_p_url = "https://books.toscrape.com/" + relative_url
            else: 
                next_p_url = "https://books.toscrape.com/catalogue/" + relative_url
            yield response.follow(next_p_url, callback= self.parse_rel_link)

    
        next_p = response.css('li.next a ::attr(href)').get()
        if next_p is not None:
            if 'catalogue/' in next_p:
                next_p = next_p.split('/')[0] + '/category/books_1/' + next_p.split('/')[1]
                next_p_url = "https://books.toscrape.com/" + next_p
            else: 
                next_p = 'catalogue/category/books_1/' + next_p.split('/')[0]
                next_p_url = "https://books.toscrape.com/" + next_p
            yield response.follow(next_p_url, callback= self.parse)



    def parse_rel_link_(self, response):

        table_rows = response.css('table tr')
        # --- without using items 
        yield {
            'url' : response.url,
            'title': response.css('prduct_main h1').get(),
            'product type': table_rows[1].css('td ::text').get(),
            'price_excl_tax': table_rows[2].css('td ::text').get(),
            'price_inclu_tax': table_rows[3].css('td ::text').get(),
            'tax': table_rows[4].css('td ::text').get(),
            'stocks avilable': table_rows[5].css('td ::text').get(),
            'reviews': table_rows[6].css('td ::text').get(),
            'stars': response.css('p.star-rating').attrib['class'],
            'category':response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description':response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price':response.css('p.price_color ::text').get()
        }
        

    def parse_rel_link(self, response):
        table_rows = response.css('table tr')
        book_item = BookItem()  # --- using item 
       
        book_item['url'] =response.url,
        book_item['title'] = response.css('prduct_main h1').get(),
        book_item['product_type'] = table_rows[1].css('td ::text').get(),
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get(),
        book_item['price_inclu_tax'] = table_rows[3].css('td ::text').get(),
        book_item['tax']= table_rows[4].css('td ::text').get(),
        book_item['stocks_avilable'] = table_rows[5].css('td ::text').get(),
        book_item['reviews'] = table_rows[6].css('td ::text').get(),
        book_item['stars']= response.css('p.star-rating').attrib['class'],
        book_item['category'] =response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] =response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] =response.css('p.price_color ::text').get()
    

  
