# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#这里设置好了字段，在后面爬取的信息才会显示出来
class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=scrapy.Field()
    name = scrapy.Field()
    avatar_url = scrapy.Field()
    headline = scrapy.Field()

    url = scrapy.Field()
    url_token = scrapy.Field()
    gender = scrapy.Field()

    type = scrapy.Field()
    badge = scrapy.Field()

    answer_count=scrapy.Field()
    articles_count=scrapy.Field()
    avatar_url_template=scrapy.Field()
    follower_count=scrapy.Field()
    is_advertiser=scrapy.Field()
    is_followed=scrapy.Field()
    is_following=scrapy.Field()
    is_org=scrapy.Field()
    user_type=scrapy.Field()

