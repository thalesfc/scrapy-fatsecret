from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import FormRequest, Request
import config
import logging
from scrapy_fatsecret.helpers import buddies


class LoginSpider(CrawlSpider):
    name = 'login_spider'
    allowed_domains = ['fatsecret.com']
    login_url = 'https://www.fatsecret.com/Auth.aspx?pa=s'
    start_urls = ['http://www.fatsecret.com/member/dorindam59']

    rules = [
        Rule(
            LinkExtractor(allow='pa=memb\&id=\d+'),
            follow=True,
            callback=buddies.parse_buddy
        )
    ]

    def start_requests(self):
        login_request = FormRequest(
            self.login_url,
            callback=self.logged,
            formdata={
                'ctl00$ctl07$Logincontrol1$Name': config.GMAIL_USER,
                'ctl00$ctl07$Logincontrol1$Password': config.PASSWORD,
                '__EVENTTARGET': 'ctl00$ctl07$Logincontrol1$Login',
                '__EVENTARGUMENT': ''
            }
        )
        return [login_request]

    def logged(self, response):
        if response.url == 'https://www.fatsecret.com/Default.aspx?pa=m':
            self.log('Successfully LOGGED.', logging.INFO)
            for url in self.start_urls:
                yield(Request(url, callback=self.parse_start_url))
        else:
            self.log('LOGIN error: ' + response.url, logging.CRITICAL)
