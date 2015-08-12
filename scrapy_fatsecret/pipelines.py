# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import json


class ValidDataPipeLine(object):
    def process_item(self, item, spider):
        for field, value in item.items():
            if not value:  # null or empty string
                raise DropItem("Missing %s in %s" % (field, item))
        return item


class JsonWriterPipeline(object):
    def __init__(self, filename):
        self.f = open(filename, 'w')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('FILE_USER_DATA'))

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.f.write(line)
        return item

    def close_spider(self, spider):
        self.f.close()
