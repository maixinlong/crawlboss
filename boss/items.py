# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class BossItem(scrapy.Item):
    position_name = Field()
    salary = Field()
    company = Field()
    company_type = Field()
    job_tags = Field()
    date = Field()
    position_desc = Field()
    address = Field()
