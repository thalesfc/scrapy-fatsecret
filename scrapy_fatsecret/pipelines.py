# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import json


class ValidDataPipeLine(object):
    def process_item(self, item, spider):
        # valid test
        for field in spider.crawler.settings.\
                get('ITEM_VALID_TESTED_FIELDS'):
            if not item[field]:
                raise DropItem("Missing %s in %s" % (field, item))

        for field, value in item.items():
            # get first element of list
            if isinstance(value, list):
                if value:
                    item[field] = value[0]
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
