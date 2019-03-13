import scrapy
from datetime import datetime

class ikmanCrawlerSpider(scrapy.Spider):
    keyword = input("Enter the product: ")
    name = "ikman_crawler"
    start_urls = [
        "https://ikman.lk/en/ads/sri-lanka/mobile-phones?query="+keyword+"&categoryType=ads"
    ]
    pageNum=0

    def parse(self, response):
        for article_title in response.css('div.item-content'):
            yield response.follow(article_title.css('div.item-content a::attr(href)').extract_first(), callback=self.parse_item_page)

        if self.pageNum==0:
            next_page = response.css('div.ui-panel-content.ui-panel-block>div.lg-g>a::attr(href)')[0].extract()
        else:
            next_page = response.css('div.ui-panel-content.ui-panel-block>div.lg-g>a::attr(href)')[1].extract()
        self.pageNum=1

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def get_int_val(str_):
        values = [int(s) for s in str_.split() if s.isdigit()]
        if len(values) > 0:
            return values[0]
        else:
            return None

    @staticmethod
    def get_year(str_):

        if len(str_) > 0:
            values = str_[0].split()
            return int(values[0])
        else:
            return None

    @staticmethod
    def get_date(str_):
        values = str_[0]
        datetime_object = datetime.strptime(values, '%d %b  %I:%M %p')
        newDate = datetime_object.replace(year = 2020)
        return newDate

    def parse_item_page(self, response):

        pricestr = response.css('div.ui-price-tag span.amount::text').extract_first().strip().replace(",", "")
        price = self.get_int_val(pricestr)

        yr_str = response.css('p.item-intro span.date::text').extract_first(),
        year_str = self.get_date(yr_str)

        yield {
        #'title':response.css('title::text').extract_first(),
        'name':response.xpath('//div/h1/text()').extract()[1],
#        'url':response.url,
        'price':price,
#        'location':response.css('p.item-intro span.location::text').extract_first(),
#        'category':response.css('div.item-content p.item-location span.item-cat::text').extract_first(),
        'date':year_str,
        #'date':response.css('p.item-intro span.date::text').extract_first(),
        'condition':response.xpath('//dl/dd/text()').extract()[0],
        'brand':response.xpath('//dl/dd/text()').extract()[1],
        'model':response.xpath('//dl/dd/text()').extract()[2],
#        'authenticity': response.xpath('//dl/dd/text()').extract()[3],
#        'seller':response.xpath('//div/p/span/a/text()').extract()[0],
        }