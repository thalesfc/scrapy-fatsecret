# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GlobalSpiderSpider(CrawlSpider):
    name = 'global_spider'
    allowed_domains = ['fatsecret.com']
    start_urls = ['http://www.fatsecret.com/Default.aspx?pa=mem&u=jilly.beans']

    rules = [
        # Extract all links and follow links from them
        # (If "allow" is not given, it will match all links.)
        Rule(LinkExtractor(), follow=True, callback='parse_item'),
    ]

    def parse_item(self, response):
        print 10 * '@', response.url
        # i = ScrapyFatsecretItem()
        # i['domain_id'] =
        #       response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] =
        #        response.xpath('//div[@id="description"]').extract()
        # return i
