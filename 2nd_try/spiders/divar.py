import scrapy

class ChetorSpider(scrapy.Spider):
    #identity
    name="divar"

    #Request
    def start_requests(self):
        url = 'https://divar.ir/s/abadeh'
        
        yield scrapy.Request(url=url, callback=self.parse)

    #Response
    def parse(self, response):
        # self.logger.info(response.request.url)
        for category in response.xpath('//li[@class="filter-category-list__item"]'):
            temp_link = category.xpath('//a[@class="filter-category-list__item-field filter-category-list__item-link"]/@href').extract_first()
            temp_link = 'https://divar.ir'+ temp_link
            yield {
                'link':'https://divar.ir'+ category.xpath('.//a[@class="filter-category-list__item-field filter-category-list__item-link"]/@href').extract_first()
            }
        
            yield scrapy.Request(url=temp_link, callback=self.parse)
        for ad in response.xpath('//div[@class="col-xs-12 col-sm-6 col-xl-4 p-tb-large p-lr-gutter post-card-item"]'):
            yield {
                'ad':'https://divar.ir' + ad.xpath('.//a[@class="post-card"]/@href').extract_first()
            } 