import scrapy
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from scrapy.linkextractors import LinkExtractor
from pymongo import MongoClient
from urllib.parse import urlencode
import math


from value_spider.items import ValueSpiderItem
# from scrapy.conf import settings
import pymongo

# df = pd.read_csv("weburls.csv")
# URLS = df[["weburl","gvkey1"]]
leftover = pd.read_csv("data.csv")


# from scraper_api import ScraperAPIClient
API_KEY = 'xxx'

def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'render': 'false', "follow_redirect": "true"}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

class Aboutspider(scrapy.Spider):
    name = "spider"

    def __init__(self, start=0, end=0,stage=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = {
            "diversity" : r'inclusion|diversity|justice|equity|equal',
            "ethic" : r'ethic|compliance|integrity',
            "esg" : r'environment|governance|responsibility|esg|sustaina|csr',
            "career" : r'career|job|employ|join|hire|work',
            "about": r'about|whoweare|profile',
            "values" : r'values|mission|vision|leadership|culture',
            "innovation" : r'innovation|tech|develop'
        }

        self.start = int(start)
        self.end = int(end)
        self.stage = int(stage) ## 0:tags; 1:homepage

    

    def start_requests(self):

        data = leftover

        for index, row in data[self.start: self.end].iterrows():
            url = row["weburl"]
            key = row["gvkey1"]
            #################### starting stage #########################################################
            # for year in range(2008, 2022): 
            #     new_url = f'https://web.archive.org/web/{year}00/{url}'.format(year, url)
            #     yield scrapy.Request(url=get_scraperapi_url(new_url), meta={'gvkey': key, 'year':year})
            #     # yield scrapy.Request(new_url, meta={'gvkey': key, 'year':year})
            #     # ultra_premium=true (75 credict)
            year = row["year"]
            new_url = f'https://web.archive.org/web/{year}/{url}'.format(year, url)
            yield scrapy.Request(url=get_scraperapi_url(new_url), meta={'gvkey': key, 'year':year})
            
        #################### hand test #########################################################
        # url = "www.bktechnologies.com"
        # key = 1117
        # for year in range(2000, 2008):
        #     new_url = f'https://web.archive.org/web/{year}00/http://{url}'.format(year, url)
        #     # yield scrapy.Request(client.scrapyGet(url=new_url), meta={'gvkey': key, 'year':year})
        #     yield scrapy.Request(url = get_scraperapi_url(new_url), meta={'gvkey': key, 'year':year})



    def parse(self, response):
        if self.stage == 0:
            for key, value in self.keywords.items():
                regexp = "\S*(" + value + ")\S*"
                regexp2 = re.compile(regexp,re.IGNORECASE)
                extractor = LinkExtractor(allow=(regexp, ))
                extractor2 = LinkExtractor(restrict_text=(regexp2, ))

                #list of Link Obje
                extracted_links = extractor.extract_links(response) + extractor2.extract_links(response)

                for link in extracted_links:
                    url = link.url
                    url = url[25:]
                    if re.search("(https?://archive.org)|(https?://help.archive.org)|(https?://www.gdeltproject.org)", url):
                        yield None
                    else:
                        yield scrapy.Request(url = get_scraperapi_url("https://web.archive.org"+ url), callback=self.parse2, meta=response.meta,cb_kwargs=dict(info_ctt=(key)))

        else:
            item = ValueSpiderItem()
            item["gvkey"] = response.meta.get("gvkey")
            item["year"] = response.meta.get("year")
            item["tag"] = "homepage"
            item["url"] = response.url
            text = response.selector.xpath('///p/text()').getall()
            text1 = response.selector.xpath('//li/text()').getall()
            text2 = response.selector.xpath('//span/text()').getall()
            text3 = response.selector.xpath('//font/text()').getall()
            text4 = response.selector.xpath('//big/text()').getall()

            clean_text = [t for t in text+text1+text2+text3+text4 if len(t)>200 and not re.search('archive', t,re.IGNORECASE)] # yes,return is selector type
            item["content"] = ""
            for i in clean_text:
                item["content"] += i
            yield item

    def parse2(self, response, info_ctt):
        item = ValueSpiderItem()
        item["tag"] = info_ctt
        item["gvkey"] = response.meta.get("gvkey")
        item["year"] = response.meta.get("year")
        if response == None:
            yield None

        item["url"] = response.url

        text = response.selector.xpath('///p/text()').getall()
        clean_text = [t for t in text if len(t)>200 and not re.search('archive', t,re.IGNORECASE)] # yes,return is selector type
        item["content"] = ""
        for i in clean_text:
            item["content"] += i
        yield item
        
    

    def handle_spider_closed(self, reason):
        self.crawler.stats.set_value('failed_urls', ', '.join(self.failed_urls))

    def extract_link(self):
        return {"name:"}

    def waybackify_url(self, url, closest_timestamp='2017'):
        return f'https://web.archive.org/web/{closest_timestamp}/{url}'

    def request_url(self,url):
        try:
            response = requests.get(url, timeout=20)
            return response
        except requests.exceptions.Timeout:
            self.report_time_out(url)
            return None
        except:
            return None
