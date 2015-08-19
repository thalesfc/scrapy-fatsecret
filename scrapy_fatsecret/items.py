# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    id = Field()
    name = Field()
    link = Field()
    weight_initial = Field()
    weight_current = Field()
    weight_target = Field()
    regime_following = Field()
    regime_performance = Field()
    description = Field()


class PostItem(Item):
    id = Field()
    link = Field()
    user_id = Field()
    date = Field()
    text = Field()
    weight_current = Field()
    weight_lost_sofar = Field()
    diet_status = Field()
    diet_current = Field()
    diet_entry = Field()
    likes = Field()
    comments = Field()
