# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.items import UserItem

import re
from urllib import unquote


def process_value(value):

    # decode html percent chars, e.g., %3f --> /
    # for some dark reasons, this function only works
    # for first level urls, so if we have 2 urls
    # embeed in one another, we have to double call it
    count = 0
    while "%" in value and count != 4:
        count += 1
        value = unquote(unquote(value))

    # 1st pre processing rule
    # consider facebook redirect
    rule = re.search("ReturnUrl=(.*)$", value)
    if rule:
        return process_value(rule.group(1))

    return value


class GlobalSpider(CrawlSpider):
    name = 'global_spider'
    allowed_domains = ['fatsecret.com']
    start_urls = ['http://www.fatsecret.com/member/losinit1655']
    # TODO change start url

    rules = [
        # 1st rule - members page
        Rule(
            LinkExtractor(
                allow=r'^(http://www\.fatsecret\.com/member/[^\/\?]+)$',
                process_value=process_value
            ),
            follow=True, callback="parse_user"
        ),

        # 2nd rule - follow everything to get links
        # Extract all links and follow links from them
        Rule(LinkExtractor(), follow=True)
    ]  # end of rules

    def parse_user(self, response):
        item = UserItem()
        item['id'] = response.url.split('/')[-1]
        item['name'] = response.xpath('//div[@class="NBBox"]/div/table/\
                tr/td[2]/div/h1/text()').extract()
        item['link'] = response.url
        return item
