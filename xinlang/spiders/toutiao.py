# # -*- coding: utf-8 -*-
# import json
# import re
# from urllib.parse import quote
#
# import scrapy
# from scrapy import Request
# import logging
# from xinlang.items import Item
# from xinlang.spiders import qs
#
# logger = logging.getLogger(__name__)
#
#
# class ToutiaoSpider(scrapy.Spider):
#     name = 'toutiao'
#     allowed_domains = ['toutiao.com']
#
#     # 不会经过allowed_domains过滤
#     def start_requests(self):
#         for q in qs:
#             for i in range(0, 100, 20):
#                 start_url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={}&format=json&keyword={}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1605182202937&_signature=_02B4Z6wo00901j67t6gAAIBBkeJhRvva1AI-vrMAANAQcVyujiIJukzj-nWpCU7EGxRyJq3iwX8NffeOWm2LxBY9abDo.TONTBJQu2Qxfw3Ej0rABG6j21IzrGfK36RExGVM.IL.Pr.NEYRs58'.format(
#                     str(i), quote(q))
#                 request = Request(start_url, callback=self.parse, meta={"q": q}, dont_filter=True)
#                 yield request
#
#     def parse(self, response):
#         meta = response.meta
#         text = response.text
#         text_dic = json.loads(text)
#         data = text_dic['data']
#         for data_piece in data:
#             if 'title' in data_piece.keys():
#                 if 'article_url' in data_piece.keys():
#                     article_url = data_piece['article_url']
#                     re_groups = re.match(r'http://toutiao.com/group/', article_url)
#                     if 'play_effective_count' in data_piece:
#                         continue
#                     if re_groups is not None:
#                         item = Item()
#                         created_time_raw = data_piece['datetime']
#                         created_time = created_time_raw.split(' ')[0]
#                         title = data_piece['title']
#                         item['title'] = title
#                         item['scheme'] = article_url
#                         item['created_at'] = created_time
#                         meta['item'] = item
#                         yield scrapy.Request(
#                             item['scheme'],
#                             callback=self.parse_detail,
#                             meta=meta
#                         )
#
#     def parse_detail(self, response):
#         q = response.meta['q']
#         ToutiaoSpider.q = q
#         item = response.meta['item']
#         item['raw_text'] = response.xpath("//p/text()").extract()
#         item['source'] = '头条'
#         logger.warning(item)
#         yield item
