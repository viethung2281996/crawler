# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from scrapy_splash import SplashRequest

from twitter.items import TwitterItem
from .twitter_crawler import TwitterCrawlerSpider

import re
import json
import time
import logging
import requests

class PostCrawlerSpider(TwitterCrawlerSpider):
  name = 'post_crawler'
  allowed_domains = ['twitter.com']
  start_urls = 'https://twitter.com'
  pages = ['/BTCTN']

  def __init__(self, name=None):
    super(PostCrawlerSpider, self).__init__(name)


if __name__ == "__main__":
  process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                    'Safari/537.36 '
  })

  process.crawl(PostCrawlerSpider)
  process.start()  # the script will block here until the crawling is finished
