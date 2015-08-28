from scrapy_fatsecret.items import FoodDiary, ExerciseDiary
from scrapy_fatsecret import common_lib
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import logging
import re


def process_member_page(response):
    url = LinkExtractor(allow='pa=mdcs(\&|$)').extract_links(response)
    if not url:
        logging.log(logging.ERROR, "View Diet not found, on " + response.url)
    else:
        url = url[0].url
        id = re.search('id=(\d+)', url).group(1)
        return Request('http://www.fatsecret.com/Diary.aspx?pa=mdc&id='
                       + id, priority=8)


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

    item['rdi'] = response.xpath('normalize-space(//div[@class="big"]\
            /text())').extract()

    return item


def parse_exercise_diary(response):
    item = ExerciseDiary()

    item['id'] = common_lib.get_page_id(response)
    item['user_id'] = common_lib.get_user_id(response)
    item['link'] = response.url
    item['date'] = response.xpath('normalize-space(\
            //div[@class="subtitle"]/text())').extract()

    summary_data = response.xpath('\
            //table[@class="generic activityValuesTbl"]\
            //td[@class="sub"]/text()').extract()
    if len(summary_data) < 2:
        logging.log(logging.WARNING, "Exercise summary data not found for\
                page %s." % response.url)
    else:
        item['summary'] = {
            'time_spent': summary_data[0],
            'calc': summary_data[1]
        }

    exercises_xpath = response.xpath('//tr[starts-with(@id, "infsec")]')
    exercises = []
    for e in exercises_xpath:
        time_spent_1 = e.xpath('.//div[@class=" activityCell bTop"]\
                /text()').extract()
        time_spent_2 = e.xpath('.//div[@class="activityCell bLeft bTop"]\
                /a/b/text()').extract()
        time_spent_3 = e.xpath('.//div[@class="activityCell bTop"]\
                /text()').extract()

        time_spent = (time_spent_1 if time_spent_1
                      else (time_spent_2 if time_spent_2 else time_spent_3))
        exercise = {
            'name': e.xpath('.//b/text()').extract()[0],
            'time_spent': time_spent[0],
            'cals': e.xpath('.//div[@class="activityCell bTop bRight"]\
                    /text()').extract()[0]
        }

        exercises.append(exercise)
    item['exercises'] = exercises

    return item
