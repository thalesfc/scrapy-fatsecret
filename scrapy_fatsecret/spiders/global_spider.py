# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.helpers import users, posts

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
    start_urls = ['http://www.fatsecret.com/member/dorindam59']
    # TODO change start url

    rules = [
        # 1st rule - members page
        Rule(
            LinkExtractor(
                allow='^http\:\/\/www\.fatsecret\.com\/member\/[^\/\?]+$',
                deny='Auth\.aspx',
                process_value=process_value
            ),
            follow=True, callback=users.parse_user
        ),

        # 2nd rule - posts: scrapy user journal posts
        Rule(
            LinkExtractor(
                allow='fatsecret\.com\/member\/[^\/\?]+\/journal',
            ),
            callback=posts.schedule_posts,
            follow=True
        )
    ]  # end of rules
