# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import json


def item_name(item):
    return item.__class__


class ValidDataPipeLine(object):
    ''' check for valid fields and for list elements return
    the first element'''
    def process_item(self, item, spider):
        # valid test
        fields = spider.crawler.settings\
            .get('ITEM_SETTINGS')[item_name(item)]['FIELD_VALIDATION']
        use_as_list = set(spider.crawler.settings.get('ITEM_SETTINGS')[
            item_name(item)]['FIELD_AS_LIST'])
        for field in fields:
            if not item[field]:
                raise DropItem("Missing %s in %s" % (field, item))

        for field, value in item.items():
            # get first element of list
            if isinstance(value, list) and field not in use_as_list:
                if value:
                    item[field] = value[0]
        return item


class JsonWriterPipeline(object):
    def __init__(self, item_settings):
        # existing items
        self.files = {key: open(value['FILENAME'], 'w')
                      for (key, value) in item_settings.items()}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('ITEM_SETTINGS'))

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.files[item_name(item)].write(line)
        return item

    def close_spider(self, spider):
        for f in self.files.values():
            f.close()
