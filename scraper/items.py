# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    site = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    company = scrapy.Field()
    job_id = scrapy.Field()
    slack = scrapy.Field()
    image_url = scrapy.Field()
