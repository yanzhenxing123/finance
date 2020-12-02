# -*- coding: utf-8 -*-
import logging
import random
import time
import datetime

import scrapy
import json

from scrapy import Request

from xinlang.items import Item
from xinlang.spiders import qs

logger = logging.getLogger(__name__)
class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']

    def start_requests(self):
        for q in qs:
            for i in range(1, 3):
                # 这里注意，不能使用中文，要改变的变量只有&kw。
                start_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%{}&page_type=searchall&page={}'.format(q, i)
                request = Request(start_url, callback=self.parse, meta={"q": q}, dont_filter=True)
                yield request

    def parse(self, response):
        meta = response.meta
        text = response.text
        res_dic = json.loads(text)
        if res_dic['ok'] == 1:
            data = res_dic['data']
            cards = data['cards']
            for card in cards:

                item = Item()
                if card['card_type'] == 9:
                    scheme = card['scheme']  # 微博链接w
                    mblog = card['mblog']
                    created_at = mblog['created_at']
                    raw_text = mblog['raw_text'].replace('\n', ",")
                    item['title'] = None
                    item['scheme'] = scheme
                    item['created_at'] = created_at
                    item['raw_text'] = raw_text
                    item['source'] = '微博'
                    meta['item']  = item
                    yield Request(
                        item['scheme'],
                        callback=self.parse_detail,
                        meta=meta,
                    )
                    time.sleep(random.randint(3, 5))
                else:
                    continue
    def parse_detail(self, response):
        item = response.meta['item']
        q = response.meta['q']
        WeiboSpider.q = q
        yield item
