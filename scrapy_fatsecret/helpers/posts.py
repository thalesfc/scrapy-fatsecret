from scrapy_fatsecret.items import PostItem
from scrapy import Request
import re


def schedule_posts(response):
    # collect user posts
    posts = response.xpath('//td[@class="borderBottom"]/h4/a/@href')\
        .extract()
    for post in posts:
        yield Request(response.urljoin(post),
                      callback=parse_post,
                      priority=7)


def parse_post(response):
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

    # calendar entry
    kcal = response.xpath('//table[@class="generic"][3]//a[1]\
        /text()').extract()
    food_status = response.xpath('normalize-space(//\
            table[@class="generic"]/tr/td[@class="smallText"][2]\
            /text())').extract()
    food_info = None
    if food_status and food_status[0]:
        food_info = re.search((
            "Fat: (\d+\.\d+\S+) \| "
            "Prot: (\d+\.\d+\S+) \| "
            "Carb: (\d+\.\d+\S+)\."), food_status[0])

    item['diet_entry'] = {
        'calories': kcal[0] if kcal else None,
        'fat': food_info.group(1) if food_info else None,
        'prot': food_info.group(2) if food_info else None,
        'carb': food_info.group(3) if food_info else None
    }

    # full html
    # TODO include html
    # item['html'] = response.body

    return item
