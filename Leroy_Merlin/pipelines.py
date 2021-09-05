# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pprint import pprint
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.http import Request


class LeroyMerlinPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client['Library'].leroy_spider

    def process_item(self, item, spider):
        my_item = dict(item)
        my_item['description'] = self.transform_char(my_item['characteristic'], my_item['value_char'])
        my_item.pop('characteristic')
        my_item.pop('value_char')
        collection = self.mongobase[spider.name]
        collection.insert_one(my_item)
        return my_item

    def transform_char(self, characteristic, value_char):
        p_value_char = []
        for i in value_char:
            a = i.replace('\n', '').replace('  ', '')
            p_value_char.append(a)
        description = dict(zip(characteristic, p_value_char))
        return description


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0] is True]

        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{item["name"]}/{image_guid}.jpg'
