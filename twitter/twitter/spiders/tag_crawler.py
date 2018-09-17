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
import urllib.parse

class TagCrawlerSpider(TwitterCrawlerSpider):
  name = 'tag_crawler'
  allowed_domains = ['twitter.com']
  start_urls = 'https://twitter.com'
  search_url = 'https://twitter.com/search?q='
  tags = ['ethereum', 'coins']

  def __init__(self, name=None):
    super(TagCrawlerSpider, self).__init__(name)

  def start_requests(self):
    base_url = self.search_url
    tag_url = ''
    for tag in self.tags:
      tag_url = tag_url + "#{}".format(tag)

    script = """
        function main(splash)
          local num_scrolls = 10
          local scroll_delay = 1.0

          local scroll_to = splash:jsfunc("window.scrollTo")
          local get_body_height = splash:jsfunc(
              "function() {return document.body.scrollHeight;}"
          )
          assert(splash:go(splash.args.url))
          splash:wait(splash.args.wait)

          for _ = 1, num_scrolls do
              scroll_to(0, get_body_height())
              splash:wait(scroll_delay)
          end        
          return splash:html()
        end 
      """ 

    tag_encode_url = urllib.parse.quote_plus(tag_url)
    url = base_url + tag_encode_url

    yield SplashRequest(url=url,
                        endpoint='execute',
                        callback = lambda r: self.parse_page(r),
                        args={'wait':2, 'lua_source': script},
                        method="GET")

if __name__ == "__main__":
  process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                    'Safari/537.36 '
  })

  process.crawl(TagCrawlerSpider)
  process.start()  # the script will block here until the crawling is finished
