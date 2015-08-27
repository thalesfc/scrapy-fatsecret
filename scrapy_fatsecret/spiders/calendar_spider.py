from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest, Request
import config
import logging
import re
from scrapy_fatsecret.helpers import calendar


def stub_process_member_page(response):
    url = LinkExtractor(allow='pa=mdcs(\&|$)').extract_links(response)
    if not url:
        logging.log(logging.ERROR, "View Diet not found, on " + response.url)
    else:
        url = url[0].url
        id = re.search('id=(\d+)', url).group(1)
        yield Request('http://www.fatsecret.com/Diary.aspx?pa=mdc&id='
                      + id, priority=8)


class CalendarSpider(CrawlSpider):
    name = 'calendar_spider'
    allowed_domains = ['fatsecret.com']
    login_url = 'https://www.fatsecret.com/Auth.aspx?pa=s'
    start_urls = ['http://www.fatsecret.com/member/dorindam59']

    rules = [
        Rule(
            LinkExtractor(
                allow='member\/[^\/\?]+$',
                deny='inweb'
            ),
            follow=True,
            callback=stub_process_member_page
        ),

        # enter calendar page
        Rule(
            LinkExtractor(
                allow='pa=mdc($|\&)'
            ),
            follow=True
        ),

        # enter food diary page
        Rule(
            LinkExtractor(allow='pa=fj($|\&)'),
            follow=False,
            callback=calendar.parse_food_diary
        )
    ]

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
            return [Request(url=u)
                    for u in self.start_urls]
        else:
            self.log('LOGIN error: ' + response.url, logging.CRITICAL)
