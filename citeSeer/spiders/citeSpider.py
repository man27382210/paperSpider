from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from citeSeer.items import CiteseerItem
import urlparse

class citeTestSpider(BaseSpider):
    name = "citeSearch"
    allowed_domains = ["citeseerx.ist.psu.edu"]
    def __init__(self, *args, **kwargs):
        super(citeTestSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_url')
        self.max_loop = 2
        self.loop     = 0  # We want it to loop 3 times so keep a class var
        self.items = []
        # self.start_urls = ["http://citeseerx.ist.psu.edu/search?q=Extracting+Noun+Phrases+in+Subject+and+Object+Roles+for+Exploring+Text+Semantics&submit=Search&sort=rlv&t=doc"]
    # start_urls = ['http://citeseerx.ist.psu.edu/search?q=Extracting+Noun+Phrases+in+Subject+and+Object+Roles+for+Exploring+Text+Semantics&submit=Search&sort=rlv&t=doc']

    def start_requests(self):  
        checkRequest = Request( 
            url      = self.start_urls, 
            meta     = {"test":"first"},
            callback = self.checker 
        )
        return [ checkRequest ]

    def checker(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="result"]')
        self.items.extend(self.parse_searchTitle(sites))
        if(self.loop<self.max_loop and response.status==200):
            print "RELOOPING", response.status, self.loop, response.meta['test']
            self.loop += 1
            urlNext = hxs.select('//div[@id="pager"]/a/@href').extract()
            urlNext = urlparse.urljoin(response.url, urlNext[0])
            checkRequest = Request(
                url = urlNext,
                callback = self.checker
            ).replace(meta = {"test":"not first"})
            return [checkRequest]
        else:
            return self.items

    def parse_searchTitle(self, sites):
        items = []
        for site in sites:
            item = CiteseerItem()
            item['title'] = site.select('h3/a[@class="remove doc_details"]/text() | h3/a[@class="remove doc_details"]/em/text()').extract()
            item['url'] = site.select('h3/a[@class="remove doc_details"]/@href').extract()[0]
            items.append(item)
        return items
