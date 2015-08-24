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
    weight = Field()
    diet = Field()
    comments = Field()
    food = Field()
    exercise = Field()
    likes = Field()


class BuddyItem(Item):
    id = Field()
    user_id = Field()
    buddies = Field()
