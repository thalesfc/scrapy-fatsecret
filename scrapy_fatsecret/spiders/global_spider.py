# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.items import UserItem
from scrapy_fatsecret.helpers import posts

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
    start_urls = ['http://www.fatsecret.com/member/dorindam59/journal']
    # TODO change start url

    rules = [
        # TODO uncomment this
        # 1st rule - members page
        # Rule(
        #     LinkExtractor(
        #         allow=r'^(http://www\.fatsecret\.com/member/[^\/\?]+)$',
        #         deny=r'Auth\.aspx',
        #         process_value=process_value
        #     ),
        #     follow=True, callback="parse_user"
        # ),

        # 2nd rule - posts: scrapy user journal posts
        Rule(
            LinkExtractor(
                allow='fatsecret\.com\/member\/[^\/\?]+\/journal',
            ),
            callback=posts.schedule_posts,
            follow=True
        )
    ]  # end of rules

    def parse_user(self, response):
        item = UserItem()
        item['id'] = response.url.split('/')[-1]
        item['name'] = response.xpath('//div[@class="NBBox"]/div/table/\
                tr/td[2]/div/h1/text()').extract()
        item['link'] = response.url

        # crawling regime information
        content = response.xpath('//div[@class="NBBox"]\
                //div[@class="bottom"][2]')
        item['weight_initial'] = content.xpath('table/tr[1]/td[2]/\
                text()').extract()
        item['weight_current'] = content.xpath('table/tr[2]/td[2]/\
                text()').extract()
        item['weight_target'] = content.xpath('table/tr[3]/td[2]/\
                text()').extract()
        item['regime_following'] = content.xpath('a[1]/text()')\
            .extract()
        item['regime_performance'] = content.xpath('a[2]/text()')\
            .extract()
        item['description'] = content.xpath('div').extract()
        return item
