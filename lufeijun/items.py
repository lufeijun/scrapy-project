# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LufeijunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LianjiaItem(scrapy.Item):
    title = scrapy.Field() # 标题
    url = scrapy.Field() #  连接
    address = scrapy.Field() # 小区
    address_region = scrapy.Field() # 区信息
    house_msg = scrapy.Field() # 房屋信息
    star_msg = scrapy.Field() # star 信息
    tag = scrapy.Field(serializer=list) # 标签
    price = scrapy.Field() # 单价 元/平
    total = scrapy.Field() # 总价 万元