
BOT_NAME = 'twitter'

SPIDER_MODULES = ['twitter.spiders']
NEWSPIDER_MODULE = 'twitter.spiders'

DOWNLOAD_DELAY = 1
# Retry many times since proxies often fail
RETRY_TIMES = 5

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 120,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 2 * 24 * 60 * 60
HTTPCACHE_GZIP = True

PROXY_LIST = 'twitter/proxy/proxy-list.txt'
# LOG_LEVEL = 'INFO'

SPLASH_URL = 'http://localhost:8050'