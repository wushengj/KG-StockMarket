# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RobinhoodItem(Item):
    url = Field()
    ticker = Field()
    company_name = Field()
    market_cap = Field()
    collections = Field()

class FintelItem(Item):
    url = Field()
    sector_GICS = Field()
    industry_SIC = Field()
    exchange = Field()
    ticker = Field()
    company_name = Field()
    country = Field()
    market_cap_M = Field()
