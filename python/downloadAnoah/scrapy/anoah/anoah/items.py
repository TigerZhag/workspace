# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnoahItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Grade(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    #period 1: pre-school; 2: primary-school; 3: junior-high-school; 4: high-school
    period = scrapy.Field()

class Subject(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    grade= scrapy.Field()

class Press(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()

class Book(scrapy.Item):
    edu_book_id = scrapy.Field()
    is_parent = scrapy.Field()
    is_expand = scrapy.Field()
    checked = scrapy.Field()
    clas = scrapy.Field()
    compatible_publish = scrapy.Field()
    name = scrapy.Field()
    publish_info = scrapy.Field()
    tree = scrapy.Field()
    tree_text = scrapy.Field()

class Tree_text(scrapy.Item):
    edition = scrapy.Field()
    grade = scrapy.Field()
    period = scrapy.Field()
    subject = scrapy.Field()
    term = scrapy.Field()
    type = scrapy.Field()
    volume_name = scrapy.Field()

class Chapter(scrapy.Item):
    edu_book_id = scrapy.Field()
    edu_chapter_id = scrapy.Field()
    name = scrapy.Field()
    parent_id = scrapy.Field()
    published_resource_total = scrapy.Field()
    tree_level = scrapy.Field()
