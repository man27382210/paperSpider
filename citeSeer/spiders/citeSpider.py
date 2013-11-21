from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from citeSeer.items import CiteseerItem

import urlparse

class citeTestSpider(BaseSpider):
    name = "citeSearch"
    def __init__(self, *args, **kwargs):
        super(citeTestSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')] 
        # self.start_urls = ["http://citeseerx.ist.psu.edu/search?q=Extracting+Noun+Phrases+in+Subject+and+Object+Roles+for+Exploring+Text+Semantics&submit=Search&sort=rlv&t=doc"]
    # allowed_domains = ["citeseerx.ist.psu.edu"]
    # start_urls = ['http://citeseerx.ist.psu.edu/search?q=Extracting+Noun+Phrases+in+Subject+and+Object+Roles+for+Exploring+Text+Semantics&submit=Search&sort=rlv&t=doc']


    def parse(self, response):
        print "response:%s \n" % response
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="result"]')
        items = []
        items.extend(self.parse_searchTitle(sites))
        url = hxs.select('//div[@id="pager"]/a/@href').extract()
        items.extend(self.parse_searchNextPage(response, url))
        # for site in sites:
        #     item = CiteseerItem()
        #     item['title'] = site.select('h3/a[@class="remove doc_details"]/text() | h3/a[@class="remove doc_details"]/em/text()').extract()
        #     item['url'] = site.select('h3/a[@class="remove doc_details"]/@href').extract()
        #     items.append(item)
        return items

    def parse_searchNextPage(self, response, nextUrl):
        url = urlparse.urljoin(response.url, nextUrl[0])
        request = Request(url)
        print "request:%s \n" % request
        hxs = HtmlXPathSelector(request)
        sites = hxs.select('//div[@class="result"]')
        items = []
        items.extend(self.parse_searchTitle(sites))
        return items

    def parse_searchTitle(self, datas):
        items = []
        for site in datas:
            item = CiteseerItem()
            item['title'] = site.select('h3/a[@class="remove doc_details"]/text() | h3/a[@class="remove doc_details"]/em/text()').extract()
            item['url'] = site.select('h3/a[@class="remove doc_details"]/@href').extract()
            items.append(item)
        return items
