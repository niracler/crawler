# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
        )
        self.db = self.connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):
        # 查看是否有spider专属的配置
        if spider.custom_settings and spider.custom_settings.get('MONGODB_COLLECTION'):
            collection = self.db[spider.custom_settings.get('MONGODB_COLLECTION')]
        else:
            collection = self.db[settings['MONGODB_COLLECTION']]

        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))
        collection.insert(dict(item))
        log.msg("Question added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item
