# -*- coding: utf-8 -*-
import random
import time

import scrapy
import logging
import re

from scrapy import Request
from xinlang.items import Item
from urllib.parse import quote, unquote

from xinlang.spiders import qs

logger = logging.getLogger(__name__)

class RenrendaiSpider(scrapy.Spider):
    name = 'renrendai'
    allowed_domains = ['sina.com.cn']

    def start_requests(self):
        for q in qs:
            start_url = 'http://search.sina.com.cn/?q={}&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=1'.format(quote(q))
            request = Request(start_url, callback=self.parse, meta={"q": q}, dont_filter=True)
            yield request

    def parse(self, response):
        div_list = response.xpath("//div[@class='box-result clearfix']")
        meta = response.meta
        # print(meta['q'])
        for div in div_list:
            item = Item()
            title_list = div.xpath(".//h2/a//text()").extract()
            title = "".join(title_list)
            item['title'] = title
            article_url = div.xpath(".//h2/a/@href").extract_first()
            item['scheme'] = article_url
            date = div.xpath(".//h2/span//text()").extract_first()
            ret = re.search(r"\d{4}-\d{2}-\d{2}", date)
            item['created_at'] = ret.group()
            meta['item'] = item
            yield scrapy.Request(
                item['scheme'],
                callback=self.parse_detail,
                meta=meta
            )

        if 'item' in meta.keys():
            meta.pop('item')

        next_url = response.xpath("//a[@title='下一页']/@href").extract_first()
        if next_url:
            next_url = "http://search.sina.com.cn/" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta=meta
            )

    def parse_detail(self, response):
        # 绑定名称
        q = response.meta['q']
        RenrendaiSpider.q = q
        item = response.meta['item']
        item['raw_text'] = response.xpath("//p/text()").extract()
        item['source'] = '新浪'
        yield item

        time.sleep(random.randint(1, 3))

