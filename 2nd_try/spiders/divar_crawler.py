import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
from random import randrange
from time import sleep


# def get_contact(_id):
#     url = 'https://api.divar.ir/v5/posts/'+_id+'/contact/'
#     payload = {}
#     headers= {}
#     # print(url)
#     response = requests.request("GET", url, headers=headers, data = payload)
#     return response.text

def my_lambda(link):
    _id = link.split('/')[-1]
    url = 'https://api.divar.ir/v5/posts/'+_id+'/contact/'
    rand_sleep = randrange(10)
    sleep(rand_sleep)
    return url

class DivarCrawlerSpider(CrawlSpider):
    name = 'divar_crawler'
    # allowed_domains = ['divar.ir/s/abadeh']
    start_urls = ['https://divar.ir/s/abadeh/']

    rules = (
        # get categories
        Rule(LinkExtractor(restrict_xpaths='//li[@class="filter-category-list__item"]'), 
                           callback='parse_item', 
                           follow=True),
        # get posts
        Rule(LinkExtractor(restrict_xpaths='//div[@class="col-xs-12 col-sm-6 col-xl-4 p-tb-large p-lr-gutter post-card-item"]'), 
                           callback='parse_item', 
                           follow=True),
            
        # get contact 
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="col-xs-12 col-sm-6 col-xl-4 p-tb-large p-lr-gutter post-card-item"]',
        #                    process_value=my_lambda ), 
        #                    callback='parse_contact', 
        #                    follow=True),

    )

    def parse_item(self, response):
        yield {
            'publish':response.xpath('//span[@class="post-header__publish-time"]/text()').extract_first(),
            'category':response.xpath('//div[@class="post-fields-item__value"][1]/text()').extract(),
            'id':response.request.url.split('/')[-1]
        }
        
    def parse_contact(self, response):
      my_response = json.loads(response.text)
      contact = my_response['widgets']['contact']['phone']
      _id = my_response['token']
      yield {
        'id' : _id,
        'contact':contact
      }
