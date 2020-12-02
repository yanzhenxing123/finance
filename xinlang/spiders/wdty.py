# -*- coding: utf-8 -*-
import json
import random
import time
from urllib.parse import quote

import scrapy
# 网贷天眼
from scrapy import Request

from xinlang.items import Item
from xinlang.spiders import qs
import re
import logging
logger = logging.getLogger(__name__)


class WdtySpider(scrapy.Spider):
    name = 'wdty'
    allowed_domains = ['p2peye.com']

    def start_requests(self):
        for q in qs:
            for i in range(1, 3):
                start_url = 'https://www.p2peye.com/search.php?mod=portal&kw={}&page={}'.format(quote(q), i)
                request = Request(start_url, callback=self.parse, meta={"q": q}, dont_filter=True)
                yield request

    def parse(self, response):
        meta = response.meta
        article_urls = response.xpath("//div[@class='result-t']/a/@href").extract()
        for article_url in article_urls:
            article_url = "https:" + article_url
            item = Item()
            item['scheme'] = article_url
            meta['item'] = item

            yield Request(
                item['scheme'],
                callback=self.parse_detail,
                meta=meta
            )

    def parse_detail(self, response):
        text2 = response.text
        q = response.meta['q']
        WdtySpider.q = q
        item = response.meta['item']
        item['raw_text'] = response.xpath("//p/text()").extract()
        item['source'] = '网贷天眼'
        item['title'] = response.xpath("//h1/text()").extract_first()
        ret = re.search(r"\d{4}-\d{2}-\d{2}", text2)
        created_at = ret.group()
        item['created_at'] = created_at
        yield item
        time.sleep(random.randint(2, 4))

