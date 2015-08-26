from scrapy_fatsecret.items import FoodDiary
from scrapy_fatsecret import common_lib
import logging


def parse_food_diary(response):
    item = FoodDiary()
    item['id'] = common_lib.get_page_id(response)
    item['user_id'] = common_lib.get_user_id(response)
    item['link'] = response.url
    item['date'] = response.xpath('normalize-space(\
            //div[@class="subtitle"]/text())').extract()

    general_info = response.xpath('//table[@class="foodsNutritionTbl"]\
            //td[@class="sub"]/text()').extract()
    if len(general_info) < 4:
        logging.log(logging.WARNING, "Could not found general food info \
                on page " + response.url)
    else:
        item['food'] = {
            'fat': general_info[0],
            'carbs': general_info[1],
            'prot': general_info[2],
            'cals': general_info[3]
        }

    dishes_xpath = response.xpath('//table\
            [@class="generic foodsNutritionTbl"]//tr[@valign="top"]')
    dishes = []
    for d in dishes_xpath:
        dish_name = d.xpath('.//b/text()').extract()
        dish_info = d.xpath('.//td[@class="normal"]')

        if len(dish_info) < 4:
            logging.log(logging.WARNING,
                        "Could not find info for food %s @ url %s" %
                        (dish_name[0], response.url))
            continue

        dish = {
            'name': dish_name,
            'fat': dish_info[0].xpath('text()').extract(),
            'carbs': dish_info[1].xpath('text()').extract(),
            'prot': dish_info[2].xpath('text()').extract(),
            'cals': dish_info[3].xpath('text()').extract()
        }
        dishes.append(dish)

    item['dishes'] = dishes

    return item
