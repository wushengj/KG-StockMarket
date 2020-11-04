'''
scrapy crawl robinhood -o <output_path>
scrapy crawl robinhood -o "../../../../data_crawled/robinhood.jl"
'''

SYM_PATH = "../../datasrc/symbols.txt"

import scrapy
from STOCKPAGEspider.items import RobinhoodItem

class STOCKPAGEspider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = 'robinhood'
    allowed_domains = ['robinhood.com']
    prefix = 'https://robinhood.com/stocks/'
    start_urls = []
    with open(SYM_PATH, 'r') as sym_f:
        lines = sym_f.readlines()
        for line in lines:
            sb = line.split('\n')[0]
            start_urls.append(prefix + sb)

    def parse(self, response):
        print('response is:', response)
        # yield from super(STOCKPAGEspider, self).parse(response)
        try:
            robinhood = RobinhoodItem()

            robinhood['url'] = response.url
            robinhood['ticker'] = response.xpath("//meta[@property='og:url']/@content").get().split('/')[-1]
            robinhood['company_name'] = response.xpath("//div[@class='row']/div[@class='col-12']/header/h1/text()").get()
            robinhood['market_cap'] = response.xpath("//div[text()='Market Cap']/parent::span/following-sibling::div[2]/text()").get()
            robinhood['collections'] = response.xpath("//span[text()='Collections']/ancestor::header/following-sibling::div[1]//span/text()").getall()

            yield robinhood

        except Exception as e:
            print('parse errrrrrrrrrrrrr', e)
            pass
