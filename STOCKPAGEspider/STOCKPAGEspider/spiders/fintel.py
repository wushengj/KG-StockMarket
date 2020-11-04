'''
scrapy crawl fintel -o <output_path>
scrapy crawl fintel -o "../../../../data_crawled/fintel.jl"
from one page, visit urls in this page, in each url, get tabular information
'''

import re

import scrapy
from STOCKPAGEspider.items import FintelItem

class STOCKPAGEspider(scrapy.Spider):
    name = 'fintel'
    allowed_domains = ['fintel.io']
    start_urls = ['https://fintel.io/industry']

    def parse(self, response):
        sector_div_list = response.xpath('//div[@class="row"]/div[@class="col" and h3]')

        for sector_div in sector_div_list:
            sector = sector_div.xpath('./h3/text()').get()
            industry_div_list = sector_div.xpath('./div/div/table/tbody/tr')
            for industry_div in industry_div_list:
                industry = industry_div.xpath('./td/a/text()').get()
                industry_url = industry_div.xpath('./td/a/@href').get() # eg: '/industry/list/coal-mining'
                print("SECTOR", sector)
                print("INDUSTRY", industry)
                print(industry_url)

                yield response.follow(industry_url, callback=self.parse_industry, meta={'sec': sector, 'ind': industry})

    def parse_industry(self, response):
        rows = response.xpath('//div/table[thead/tr/th/text()="Exchange"]/tbody/tr')

        for row in rows:
            row_text = row.xpath('./td[not(@style)]/text()').getall()

            fintel = FintelItem()

            fintel['url'] = row.xpath('./td/a/@href').get()
            fintel['sector_GICS'] = response.meta['sec']
            fintel['industry_SIC'] = response.meta['ind']
            if len(row_text) == 3:
                fintel['exchange'] = row_text[0]
                fintel['ticker'] = row_text[1]
                fintel['country'] = row_text[2]
            elif len(row_text) == 2:
                fintel['exchange'] = None
                fintel['ticker'] = row_text[0]
                fintel['country'] = row_text[1]
            else:
                print(row, response.meta['sec'], response.meta['ind'], row)
                break

            fintel['company_name'] = row.xpath('./td/a/text()').get()
            market_cap = row.xpath('./td[@style="text-align: right"]/text()').get()
            if market_cap != None:
                fintel['market_cap_M'] = int(re.sub('[, ]', '', market_cap))
            else:
                fintel['market_cap_M'] = None

            yield fintel

