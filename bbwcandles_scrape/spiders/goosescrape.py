import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider 
from datetime import datetime
import os
#rom bbwcandles_scrape.items import BbwcandlesScrapeItem
today = datetime.today().strftime('%Y-%m-%d')
import logging

class GoosescrapeSpider(CrawlSpider):
#class GoosescrapeSpider(scrapy.Spider):    
    name = "goosescrape"
    allowed_domains = ["goosecreekcandle.com"]
    start_urls = ["https://goosecreekcandle.com"]
    base_url = "https://goosecreekcandle.com"
    #rules = [Rule(LinkExtractor(restrict_xpaths="//a[@class='page-link']"), callback= "parse", follow=True)]
    rules = [Rule(LinkExtractor(allow='/collections/'), callback= "parse", follow=True)]
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GoosescrapeSpider, cls).from_crawler(crawler, *args, **kwargs)
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #output_file = f'E:Documents//GitHub_Repositories//Sephora//bbwcandles_scrape//bbwcandles_scrape//spiders//outputs//scrapped_{spider.name}_{date_str}.json'
        base_output_dir = os.getenv('OUTPUT_DIR', '/app/data')  # Default to /app/data if not specified
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(base_output_dir, f'scrapped_{spider.name}_{date_str}.json')
        crawler.settings.set('FEED_URI', output_file, priority='cmdline')
        crawler.settings.set('FEED_FORMAT', 'json', priority='cmdline')
        logging.info(f"Setting FEED_URI to: {output_file}")
        return spider
    
    def parse(self, response):

        dict1={"Product Main Category":""}
        dict2={"Product Sub-Category":""}

        required={'/collections/strawberry-shortcake-goose-creek', '/collections/scented-plug-ins',
                '/collections/care-bears-x-goose-creek', '/collections/little-debbie-x-goose-creek-candles', 
                '/pages/gift-goose-creek-candles', '/collections/willy-wonka-x-goose-creek',
                    '/collections/new-arrivals',  '/collections/room-sprays', 
                    '/collections/wax-melts', '/collections/odor-control-candles','/collections/all-body-care-products', '/collections/sale',
                        '/collections/world-traveler-candles', '/collections/peter-rabbit-goose-creek', 
                        '/collections/essential-oils-100-natural-pure',  '/collections/candy-land-x-goose-creek'}
                   
        for link in set(response.xpath("//li[@class='dropdown mega-menu']/div/a/@href")):
            if '/candles' in link.get():
                href=link.get()
                dict1["Product Main Category"] = href.split('/')[-1]
                yield response.follow(link)
                for link1 in response.xpath("//div[@class='banner-filter']/a/@href"):
                    dict2["Product Sub-Category"] = response.xpath("//div[@class='title-bar custom-font collection-header']/h2/text()").get()
                    yield response.follow(link1)
                    for link2 in response.xpath("//div[@class='hp-title']/a/@href"):
                        yield response.follow(link2, self.product_parse, meta={'dict1': dict1, 'dict2': dict2})
            else:
                for link in required:
                    dict1["Product Main Category"] = response.xpath("//span[@class='nav-label']/text()").get()
                    yield response.follow(link)
                    dict2["Product Sub-Category"] = response.xpath("//div[@class='title-bar custom-font collection-header']/h2/text()").get()
                    for link2 in response.xpath("//div[@class='hp-title']/a/@href"):
                        yield response.follow(link2, self.product_parse,meta={'dict1': dict1, 'dict2': dict2})
                        yield response.follow(link2, self.product_parse,meta={'dict1': dict1, 'dict2': dict2})

    def product_parse(self,response):
        # main product category: response.xpath("//span[@class='nav-label']/text()").getall()
        dict1 = response.meta.get('dict1', {})
        dict2 = response.meta.get('dict2', {})
        yield{
            "Scrapped_On": today,
            **dict1,
            **dict2,
            "title" : response.xpath("//div[@class='mobile-info-container']/p[@class='custom-font product-description-header']/text()").get(),
            "rating" : response.xpath("//div[@class='oke-sr-rating']/text()").get(),
            "numReviews" : response.xpath("//div[@class='oke-sr-count']/span[@class='oke-sr-count-number']/text()").get(),
            "price_now" : response.xpath("//span[@class='money']/text()").get(), #product-page--pricing--variant-compare-at-price
            "price_earlier" : response.xpath("//li[@class='product-page--pricing--variant-compare-at-price']/span/span/text()").get(),
            "Details" : response.xpath("//div[@class='metafield-rich_text_field']/p[last()]/text()").get(),
            "5_star_Rating":response.xpath("//div[@class='oke-w-breakdownModule-distribution-count'][1]/text()").get(),
            "4_star_Rating":response.xpath("//div[@class='oke-w-breakdownModule-distribution-count'][2]/text()").get(),
            "3_star_Rating":response.xpath("//div[@class='oke-w-breakdownModule-distribution-count'][3]/text()").get(),
            "2_star_Rating":response.xpath("//div[@class='oke-w-breakdownModule-distribution-count'][4]/text()").get(),
            "1_star_Rating":response.xpath("//div[@class='oke-w-breakdownModule-distribution-count'][5]/text()").get()
        }
