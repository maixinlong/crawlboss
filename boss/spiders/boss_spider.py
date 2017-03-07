#! /usr/bin/env python
#coding=utf-8


from scrapy.spider import Spider
from scrapy.selector import Selector
from boss.items import BossItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.http import Request
import time

class Boss2(Spider):
    name = "boss1"
    start_urls = [
        #"https://www.zhipin.com/job_detail/",
        #"https://www.zhipin.com/job_detail/?query=python&scity=101010100&source=2",
        "https://www.zhipin.com/c101010100/h_101010100/?query=python&page=1",
    ]
    
    def parse(self,response):
        #print response.body
        sel = Selector(response)
        sites = sel.xpath('//div[@class="job-primary"]')
        items = []
        for site in sites:
            item = BossItem()
            item["position_name"] = site.xpath('div[@class="info-primary"]/h3/text()').extract()[0]
            item["salary"] = site.xpath('div[@class="info-primary"]/h3/span/text()').extract()[0]
            item["company"] = site.xpath('div[@class="info-comapny"]/div/h3/text()').extract()[0]
            item["company_type"] = site.xpath('div[@class="info-comapny"]/div/p/text()').extract()[0]
            items.append(item)
        return items
    
    
"""
继承CrawlSpider 实现爬取多层页面
"""    

class Boss3(CrawlSpider):
    name = "boss3"
    allowed_domains = ["zhipin.com"]
    start_urls = [
        "https://www.zhipin.com/c101010100/h_101010100/?query=python&page=1"
    ]    
    rules = [
        Rule(SgmlLinkExtractor(allow=(r'query=python&page=.*',)),callback='parse_next_page'),
    ]
    
    
    def parse_next_page(self,response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="job-primary"]')
        items = []
        for site in sites:
            item = BossItem()
            item["position_name"] = site.xpath('div[@class="info-primary"]/h3/text()').extract()[0]
            item["salary"] = site.xpath('div[@class="info-primary"]/h3/span/text()').extract()[0]
            item["company"] = site.xpath('div[@class="info-comapny"]/div/h3/text()').extract()[0]
            item["company_type"] = site.xpath('div[@class="info-comapny"]/div/p/text()').extract()[0]
            #items.append(item)
            yield item
            print item["position_name"]
        #return items
            

alread_urls = set()

class Boss(BaseSpider):
    name = "boss"
    allowed_domains = ["zhipin.com"]
    start_urls = ["https://www.zhipin.com/c101010100/h_101010100/?query=python&page=1"]
    
    def parse(self,response):
        sel = Selector(response)
        sites = sel.xpath('//li/a')
        items = []
        for site in sites:
            if not site.xpath('div[@class="job-primary"]'):
                continue
            item = BossItem()
            item["position_name"] = site.xpath('div[@class="job-primary"]/div[@class="info-primary"]/h3/text()').extract()[0]
            item["salary"] = site.xpath('div[@class="job-primary"]/div[@class="info-primary"]/h3/span/text()').extract()[0]
            item["company"] = site.xpath('div[@class="job-primary"]/div[@class="info-comapny"]/div/h3/text()').extract()[0]
            item["company_type"] = site.xpath('div[@class="job-primary"]/div[@class="info-comapny"]/div/p/text()').extract()
            item["job_tags"] = site.xpath('div[@class="job-tags"]/span/text()').extract()
            position_url = "https://www.zhipin.com"+site.xpath('@href').extract()[0]
            yield Request(position_url,meta={'item':item},callback=self.parse_position_info)
            #yield item
        urls = sel.xpath('//div[@class="page"]/a/@href').extract()
        urls = []
        for url in set(urls):
            if 'javascript' not in url and url not in alread_urls:
                print "++"*5,url
                alread_urls.add(url)
                url = "https://www.zhipin.com"+url
                time.sleep(5)
                yield Request(url,callback=self.parse)
    
    def parse_position_info(self,response):
        time.sleep(4)
        item = response.meta['item']
        sel = Selector(response)
        address = ""
        try:
            address = sel.xpath('//div[@class="location-address"]/text()').extract()[0]
        except:
            print "address is null"
        item["address"] = address
        position_desc = sel.xpath('//div[@class="text"]/text()').extract()
        desc = u""
        for i in position_desc:
            desc += i.strip()
        item["position_desc"] = desc
        yield item
            
        
    
    