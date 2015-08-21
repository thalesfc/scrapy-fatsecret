def get_user_id(response):
    return response.xpath('//div[@class="breadcrumb_link"][3]\
            /a/@title').extract()
