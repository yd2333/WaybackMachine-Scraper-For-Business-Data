# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

class Aboutspider(scrapy.Spider):
    def __init__(self, start=2000, end=2021, collection=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = {
            "diversity" : r'inclusion|diversity|justice|equity',
            "ethic" : r'ethic|compliance|integrity',
            "esg" : r'environment|governance|responsibility|esg|sustaina|csr',
            "career" : r'career|job|employ|join|hire',
            "about": r'about|whoweare',
            "values" : r'values|mission|vision|leadership|culture',
            "innovation" : r'innovation'
        }
