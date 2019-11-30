# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymongo


class TiebaPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(connect=False)
        db = client['users']
        self.dataCollection = db['tieba']

    def process_item(self, item, spider):
        self.dataCollection.insert_one(dict(item))


