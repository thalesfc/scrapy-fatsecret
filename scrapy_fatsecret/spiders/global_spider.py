# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.items import UserItem


class GlobalSpiderSpider(CrawlSpider):
    name = 'global_spider'
    allowed_domains = ['fatsecret.com']
    start_urls = ['http://www.fatsecret.com/Default.aspx?pa=mem&u=jilly.beans']
    # TODO change start url

    rules = [
        # Extract all links and follow links from them
        # (If "allow" is not given, it will match all links.)
        # Rule(LinkExtractor(), follow=True),
        # TODO uncomment this

        # follow members page
        Rule(
            LinkExtractor(
                allow=r'member/\S+',
                ), follow=True, callback="parse_user")
        # TODO change follow to true
    ]

    def parse_user(self, response):
        item = UserItem()
        item['id'] = response.url.split('/')[-1]
        item['name'] = response.xpath('//div[@class="NBBox"]/div/table/\
                tr/td[2]/div/h1/text()').extract()
        item['link'] = response.url
        yield item
