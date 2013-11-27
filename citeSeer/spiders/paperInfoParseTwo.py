from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from citeSeer.items import CiteseerPaperItem
import urlparse

class citePaperSpider(BaseSpider):
    name = "citePaperParseTwo"
    allowed_domains = ["citeseerx.ist.psu.edu"]
    pipelines = ['MongoDBPipeline']
    def __init__(self, *args, **kwargs):
        super(citePaperSpider, self).__init__(*args, **kwargs)
        self.start_urls = "http://citeseerx.ist.psu.edu"+kwargs.get('start_url')
        # self.url = kwargs.get('start_url')
        # self._id = kwargs.get('start_url').split('=')[1]
        # self.title = ""
        # self.abs = ""
        # self.refs = {}
        # self.cites = []

    def start_requests(self):               
        checkRequest = Request( 
            url      = self.start_urls, 
            meta     = {"level":0},
            callback = self.parserPaper 
        )
        return [ checkRequest ]

    def parserPaper(self, response):
        level = response.meta['level']
        print "level : %s " % level
        if level < 6:
            paper = CiteseerPaperItem()
            hxs = HtmlXPathSelector(response)
            paper['title'] = hxs.select('//div[@id="viewHeader"]/h2/text()').extract()[0]
            refs = hxs.select('//div[@id="citations"]/table/tr')
            paper['defpaper'] = self.parse_ref(refs)
            # citeUrl = hxs.select('//div[@id="pager"]/a/@href').extract()[0]
            # yield Request(url = "http://citeseerx.ist.psu.edu"+citeUrl, meta = {"paper":paper, "self":self}, callback = self.parser_cite)
            yield paper
            for ref in paper['defpaper']:
                yield Request(url = "http://citeseerx.ist.psu.edu"+ref['url'], meta = {"level":level+1}, callback = self.parserPaper)
            # yield self.extractData(paper)
            # print "paper :%s " % paper
            
        else:
            pass
            # return self.extractData()
            # return paper

    def parse_ref(self, refsInPaper):
        refsArray = []
        for ref in refsInPaper:
            refTitle = ref.select('td/a/text()').extract()[0]
            refUrl = ref.select('td/a/@href').extract()[0]
            refID = refUrl.split('=')[1]
            refDic = {"_id":refID, "title":refTitle, "url":refUrl}
            refsArray.append(refDic)
        return refsArray
        
    def parser_cite(self, response):
        paper = response.meta['paper']
        self = response.meta['self']
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="result"]')
        paper['citebypaper'].extend(self.parse_citeTitle(sites))
        urlNext = hxs.select('//div[@id="pager"]/a/@href').extract()[0]
        if urlNext:
            urlNext = "http://citeseerx.ist.psu.edu"+urlNext
            checkRequest = Request(
                url = urlNext,
                paper = paper,
                self = self,
                callback = self.parser_cite
            )
            return [ checkRequest ]
        else:
            return self.extractData()

    def parse_citeTitle(self, cites):
        items = []
        for cite in cites:
            title = cite.select('h3/a[@class="remove doc_details"]/text() | h3/a[@class="remove doc_details"]/em/text()').extract()[0]
            url = cite.select('h3/a[@class="remove doc_details"]/@href').extract()[0]
            item = {"title":title, "url":url}
            items.append(item)
        return items


    def extractData(self, paper):
        print "paper : %s" % paper
        # paper = CiteseerPaperItem()
        # paper['_id'] = self._id
        # paper['title'] = self.title
        # paper['abstart'] = self.abs
        # paper['defpaper'] = self.refs
        # paper['citebypaper'] = self.cites
        return paper
    
