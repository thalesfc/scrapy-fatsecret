# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.helpers import users, posts, buddies, calendar
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
                allow='member\/[^\/\?]+$',
                deny='inweb'  # deny my own user
            ),
            follow=True,
            callback='parse_member'
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
        ),

        # 4th rule [LOGGED, MAIN_PAGE] - diary: go to main dairy page
        Rule(
            LinkExtractor(
                allow='pa=mdc($|\&)'
            ),
            follow=True
        ),

        # 5th rule [LOGGED] - food diary
        Rule(
            LinkExtractor(allow='pa=fj($|\&)'),
            follow=False,
            callback=calendar.parse_food_diary
        ),

        # 6th rule [LOGGED] - exercise diary
        Rule(
            LinkExtractor(allow='pa=aj($|\&)'),
            follow=False,
            callback=calendar.parse_exercise_diary
        ),
    ]  # end of rules

    def parse_member(self, response):
        # scrapy members info
        yield users.parse_user(response)
        # scrapy diary page
        yield calendar.process_member_page(response)

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
