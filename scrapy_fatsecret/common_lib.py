import re


def get_user_id(response):
    return response.xpath('//div[@class="breadcrumb_link"][3]\
            /a/@title').extract()


def get_page_id(response):
    return re.search("id=(\d+)", response.url).group(1)
