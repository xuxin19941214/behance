# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BehanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #策展库里的分类
    Li_classes = scrapy.Field()
    #策展库里的图片集名字
    Li_name = scrapy.Field()
    #策展库里图片集的设计者
    Li_designer = scrapy.Field()
    #策展库里图片链接
    Li_img_list = scrapy.Field()
    #创意工具里的分类
    To_classes = scrapy.Field()
    #创意工具里的图片集名字
    To_name = scrapy.Field()
    #创意工具里图片集的设计者
    To_designer = scrapy.Field()
    #创意工具里图片链接
    To_img_list = scrapy.Field()
    #学校和组织里的分类
    Or_classes = scrapy.Field()
    #学校和组织里的图片集名字
    Or_name = scrapy.Field()
    #学校和组织里图片集的设计者
    Or_designer = scrapy.Field()
    #学校和组织里图片链接
    Or_img_list = scrapy.Field()
