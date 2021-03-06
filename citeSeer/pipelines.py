import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem

import json

class MongoDBPipeline(object):
    def __init__(self):
        conn = pymongo.Connection(settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if spider.name != "citeSearch":
            self.collection.insert(dict(item))
        return item



class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item