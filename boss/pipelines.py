# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BossPipeline(object):
    
    def __init__(self):
        self.db = pymongo.Connection()['scrapy']['boss']
    
    def process_item(self, item, spider):
        item['job_tags'] = '|'.join(item['job_tags'])
        item['company_type'] = '|'.join(item['company_type'])
        self.db.insert(dict(item))
        return item
