# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.conf import settings
from scrapy import Request
from scrapy_splash import SplashRequest

from twitter.items import TwitterItem

import re
import json
import time
import logging
import requests

class TwitterCrawlerSpider(CrawlSpider):
  name = 'twitter_crawler'
  allowed_domains = ['twitter.com']
  start_urls = 'https://twitter.com'
  pages = ['/BTCTN']

  def __init__(self, name=None):
    super(TwitterCrawlerSpider, self).__init__(name)

  def start_requests(self):
    base_url = self.start_urls
    for page in self.pages:
      page_url = base_url + page
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
      yield SplashRequest(url=page_url,
                          endpoint='execute',
                          callback = lambda r: self.parse_page(r),
                          args={'wait':2, 'lua_source': script},
                          method="GET")


  def parse_page(self, response): 
    base_url = self.start_urls      
    posts = response.xpath(
      '//li[contains(@class, "stream-item")]\
      //div[contains(@class, "has-content")]\
      /@data-permalink-path').extract()

    for post in posts:
      post_url = base_url + str(post)
      yield Request(url=post_url,
                    callback = lambda r: self.parse_post(r),
                    method="GET")

  def get_page_name(self, response):
    page_name = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "content clearfix")]\
      //a\
      //span[contains(@class, "FullNameGroup")]\
      //strong\
      /text()').extract_first()
    return str(page_name)

  def get_short_link(self, response):
    short_link = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "text-container")]\
      //p\
      //a[contains(@class, "twitter-timeline-link")]\
      /@href').extract_first()
    return str(short_link)

  def get_description(self, response):
    description = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "text-container")]\
      //p\
      /text()').extract_first()
    return str(description)

  def get_time(self, response):
    time = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "tweet-details")]\
      //div[contains(@class, "client-and-actions")]\
      //span\
      //span\
      /text()').extract_first()
    return str(time)

  def get_reply(self, response):
    reply = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "stream-item-footer")]\
      //div[contains(@class, "ProfileTweet-actionList ")]\
      //div[contains(@class, "ProfileTweet-action--reply")]\
      //span[contains(@class, "ProfileTweet-actionCount")]\
      //span\
      /text()').extract_first() or 0
    return str(reply)

  def get_retweet(self, response):
    retweet = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "stream-item-footer")]\
      //div[contains(@class, "ProfileTweet-actionList ")]\
      //div[contains(@class, "ProfileTweet-action--retweet")]\
      //span[contains(@class, "ProfileTweet-actionCount")]\
      //span\
      /text()').extract_first() or 0
    return str(retweet)

  def get_favorite(self, response):
    favorite = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "stream-item-footer")]\
      //div[contains(@class, "ProfileTweet-actionList ")]\
      //div[contains(@class, "ProfileTweet-action--favorite")]\
      //span[contains(@class, "ProfileTweet-actionCount")]\
      //span\
      /text()').extract_first() or 0
    return str(favorite)

  def get_image(self, response):
    image = response.xpath(
      '//div[contains(@class, "permalink-tweet-container")]\
      //div[contains(@class, "has-content")]\
      //div[contains(@class, "AdaptiveMediaOuterContainer")]\
      //div[contains(@class, "AdaptiveMedia-container")]\
      //div[contains(@class, "AdaptiveMedia-singlePhoto")]\
      //div[contains(@class, "AdaptiveMedia-photoContainer")]\
      //img\
      /@src').extract_first()
    return str(image)

  def parse_post(self, response):
    posturl = response.url

    twitter = TwitterItem()

    twitter['url'] = posturl
    twitter['page_name'] = self.get_page_name(response)
    twitter['description'] = self.get_description(response)
    twitter['short_link'] = self.get_short_link(response)
    twitter['image'] = self.get_image(response)
    twitter['time'] = self.get_time(response)
    twitter['reply'] = self.get_reply(response)
    twitter['retweet'] = self.get_retweet(response)
    twitter['favorite'] = self.get_favorite(response)

    yield twitter

if __name__ == "__main__":
  process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                    'Safari/537.36 '
  })

  process.crawl(TwitterCrawlerSpider)
  process.start()  # the script will block here until the crawling is finished
