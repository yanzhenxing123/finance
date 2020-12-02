"""
@Author: yanzx
@Date: 2020/11/22 22:06
@Description: 
"""

import time
import os

while True:
    os.system("scrapy crawlall")
    time.sleep(86400)  #每隔一天运行一次 24*60*60=86400s
