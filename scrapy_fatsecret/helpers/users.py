from scrapy_fatsecret.items import UserItem


def parse_user(response):
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
    item['description'] = content.xpath('normalize-space(div)').extract()
    return item
