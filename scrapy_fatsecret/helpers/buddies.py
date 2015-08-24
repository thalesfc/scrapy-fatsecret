from scrapy_fatsecret.items import BuddyItem
from scrapy_fatsecret import common_lib


def parse_buddy(response):
    item = BuddyItem()
    item['id'] = common_lib.get_page_id(response)
    item['user_id'] = common_lib.get_user_id(response)

    buddies = response.xpath('//b/a[@class="member"]')
    item['buddies'] = [
        b.xpath('normalize-space(text())').extract()
        for b in buddies
    ]
    yield item
