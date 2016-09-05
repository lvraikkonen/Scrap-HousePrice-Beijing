# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoldHouseItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()  # 小区 大小
    house_info = scrapy.Field()  # 朝向 装修
    deal_data = scrapy.Field()  # 成交日期
    total_price = scrapy.Field()  # 总价
    position_icon = scrapy.Field()  # 低楼层 2007年 塔楼
    unit_price = scrapy.Field()  # 单价
    deal_house_txt = scrapy.Field()  # 满5年
    sell_flag = scrapy.Field()


class HouseItem(scrapy.Item):
    total_price = scrapy.Field()  # 总价
    unit_price = scrapy.Field()  # 单价
    down_payment = scrapy.Field()  # 首付
    tax = scrapy.Field()  # 税费
    house_type = scrapy.Field()  # 居室
    house_year = scrapy.Field()
    house_layout = scrapy.Field()  # 楼层
    house_direction = scrapy.Field()  # 朝向
    house_decorate = scrapy.Field()  # 装修
    house_area = scrapy.Field()  # 面积
    house_fact_area = scrapy.Field()  # 实际面积
    house_begin_sell = scrapy.Field()  # 挂牌时间
    house_purpose = scrapy.Field()  # 房屋用途
    house_transacton = scrapy.Field()  # 交易权属
    house_full_five = scrapy.Field()  # 满5年
    house_unique = scrapy.Field()  # 是否唯一
    community_name = scrapy.Field()  # 小区名称
    area_name = scrapy.Field()  # 地理位置
    school_name = scrapy.Field()  # 学校
    morgage = scrapy.Field()  # 是否抵押
    sell_flag = scrapy.Field()
    page_url = scrapy.Field()
