# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fatsecret.items import UserItem, PostItem
from scrapy import Request

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

        # 2nd rule - scrapy user feed
        Rule(
            LinkExtractor(
                allow='fatsecret\.com\/member\/[^\/\?]+\/journal',
            ),
            callback='schedule_posts',
            follow=True
        )
    ]  # end of rules

    def schedule_posts(self, response):
        # collect user posts
        posts = response.xpath('//td[@class="borderBottom"]/h4/a/@href')\
            .extract()
        for post in posts:
            yield Request(response.urljoin(post),
                          callback=self.parse_post,
                          priority=7)

    def parse_post(self, response):
        item = PostItem()
        item['id'] = re.search("id=(\d+)", response.url).group(1)
        item['link'] = response.url
        item['user_id'] = response.xpath('//div[@class="breadcrumb_link"][3]\
                /a/@title').extract()
        item['date'] = response.xpath('//div[@class="breadcrumb_noLink"]/\
                text()').extract()

        # textual fields
        content = response.xpath('//table[@class="generic breakout"]')
        item['text'] = content.xpath('normalize-space(tr/td/div[2]/text())')\
            .extract()
        item['weight_current'] = content.xpath('tr/td/div[3]/table/tr/\
                td[2]/span[1]/text()').extract()
        item['weight_lost_sofar'] = content.xpath('tr/td/div[3]/table/tr/\
                td[2]/span[2]/b/text()').extract()
        item['diet_status'] = content.xpath('normalize-space(tr/td/div[3]\
                /table/tr/td[2]/text()[4])').extract()
        if item['diet_status']:
            item['diet_status'] = item['diet_status'][0].strip()
        item['diet_current'] = content.xpath('normalize-space(tr/td/div[3]\
                //div[@class="smallText"][2]/a/text())').extract()

        # comments
        comments_xpath = response.xpath('//tr[@class="listrow"]/td')
        comments = []
        for comment_xpath in comments_xpath:
            comment = {
                'user_id': comment_xpath.xpath('div[2]/a/text()').extract(),
                'date': " ".join(comment_xpath.xpath('normalize-space(div[2]\
                        /text())').extract()[0].split()[:3]),
                'text': comment_xpath.xpath('normalize-space(div[1]/text())')
                .extract()[0]
            }
            comments.append(comment)
        item['comments'] = comments

        # full html
        # TODO include html
        # item['html'] = response.body

        return item

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
