# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.helpers import users, posts, buddies
from scrapy import FormRequest, Request
import config
import logging


class GlobalSpider(CrawlSpider):
    name = 'global_spider'
    allowed_domains = ['fatsecret.com']
    login_url = 'https://www.fatsecret.com/Auth.aspx?pa=s'
    start_urls = ['http://www.fatsecret.com/member/dorindam59']

    rules = [
        # 1st rule - members page
        Rule(
            LinkExtractor(
                allow='^http\:\/\/www\.fatsecret\.com\/member\/[^\/\?]+$'
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
        ),

        # 3rd rule [LOGGED] - buddies: scrapy users' friends
        Rule(
            LinkExtractor(allow='pa=memb', deny='(order=|pg=0)'),
            follow=True,
            callback=buddies.parse_buddy
        )
    ]  # end of rules

    # start request is used to process files instead of start_urls
    # we are using it to log our spider on the website
    def start_requests(self):
        return [
            FormRequest(
                self.login_url,
                formdata={
                    'ctl00$ctl07$Logincontrol1$Name': config.GMAIL_USER,
                    'ctl00$ctl07$Logincontrol1$Password': config.PASSWORD,
                    '__EVENTTARGET': 'ctl00$ctl07$Logincontrol1$Login',
                },
                callback=self.after_login
            )
        ]

    def after_login(self, response):
        if response.url == 'https://www.fatsecret.com/Default.aspx?pa=m':
            self.log('Successfully LOGGED.', logging.INFO)
            return [Request(url=u) for u in self.start_urls]
        else:
            self.log('LOGIN error: ' + response.url, logging.CRITICAL)
