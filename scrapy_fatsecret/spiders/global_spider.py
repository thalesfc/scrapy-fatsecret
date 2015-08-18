# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.helpers import users, posts


class GlobalSpider(CrawlSpider):
    name = 'global_spider'
    allowed_domains = ['fatsecret.com']
    start_urls = ['http://www.fatsecret.com/member/dorindam59']
    # TODO change start url

    rules = [
        # 1st rule - members page
        Rule(
            LinkExtractor(
                allow='^http\:\/\/www\.fatsecret\.com\/member\/[^\/\?]+$'
            ),
            follow=False, callback=users.parse_user
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
