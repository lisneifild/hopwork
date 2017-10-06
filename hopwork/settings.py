# -*- coding: utf-8 -*-
import os

# Project absolute path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Scrapy settings for hopwork project
BOT_NAME = 'hopwork'

SPIDER_MODULES = ['hopwork.spiders']
NEWSPIDER_MODULE = 'hopwork.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 0

# Enable http cookies
COOKIES_ENABLED = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6,uk;q=0.4,und;q=0.2',
  'Referer': 'https://www.hopwork.fr',
  'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
   # 'random_useragent.RandomUserAgentMiddleware': 400
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'hopwork.pipelines.HopworkPipeline': 300,
}

# Show skipped requests
DUPEFILTER_DEBUG = True