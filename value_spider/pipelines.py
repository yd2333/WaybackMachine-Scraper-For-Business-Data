# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import sys
from .items import ValueSpiderItem
import re
import pandas as pd 
import csv


class MongoDBPipeline:
    collection = 'NeedFill'

    def __init__(self, mongodb_uri, mongodb_db, mongodb_collection):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        # self.mongodb__collection = mongodb_collection
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items'),
            mongodb_collection=crawler.settings.get('MONGODB_COLLECTION', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # data = dict(ValueSpiderItem(item))
        # clean the content that is empty or lead with archive domain
        content = item["content"]
        if content == "" or re.search("^(https?://archive.org)|(https?://help.archive.org)|(https?://www.gdeltproject.org)", item["url"]):
            return
        else:
            myquery = {"gvkey":item["gvkey"],"year":item["year"]}
            # old = self.db[self.collection].find_one(myquery)[item["tag"]]
            # newvalues = { "$set": { item["tag"]: old+content } }
            newvalues = { "$set": { item["tag"]: content } }
            self.db[self.collection].update_one(myquery, newvalues)
            return item
            



class ValueSpiderPipeline:
    def process_item(self, item, spider):
        return item
