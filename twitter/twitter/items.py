import scrapy
from scrapy.item import Field

class TwitterItem(scrapy.Item):
  url = Field()
  page_name = Field()
  description = Field()
  short_link = Field()
  image = Field()
  time = Field()
  reply = Field()
  retweet = Field()
  favorite = Field()