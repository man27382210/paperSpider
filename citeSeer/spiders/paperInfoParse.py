from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from citeSeer.items import CiteseerPaperItem
import urlparse

class citePaperSpider(BaseSpider):
    name = "citePaperParse"
    allowed_domains = ["citeseerx.ist.psu.edu"]
    pipelines = ['MongoDBPipeline']
    def __init__(self, *args, **kwargs):
        super(citePaperSpider, self).__init__(*args, **kwargs)
        self.start_urls = "http://citeseerx.ist.psu.edu"+kwargs.get('start_url')
        self.url = kwargs.get('start_url')
        self._id = kwargs.get('start_url').split('=')[1]
        self.title = ""
        self.abs = ""
        self.refs = {}
        self.cites = []


    def start_requests(self):               
        checkRequest = Request( 
            url      = self.start_urls, 
            meta     = {"level":0},
            callback = self.checker 
        )
        return [ checkRequest ]

    def checker(self, response):
        hxs = HtmlXPathSelector(response)
        self.title = hxs.select('//div[@id="viewHeader"]/h2/text()').extract()[0]
        self.abs = hxs.select('//div[@id="abstract"]/p').extract()[0]
        refs = hxs.select('//div[@id="citations"]/table/tr')
        self.parse_ref(refs, "0")
        for ref in self.refs["0"]:
            yield Request(url = "http://citeseerx.ist.psu.edu"+ref['url'], meta = {"level":"1", "self":self},callback = self.parserRef)

    def parse_ref(self, refsInPaper, level):
        refsInLevel = []
        arrayUse = []
        for ref in refsInPaper:
            refTitle = ref.select('td/a/text()').extract()[0]
            refUrl = ref.select('td/a/@href').extract()[0]
            refDic = {"title":refTitle, "url":refUrl}
            refsInLevel.append(refDic)
        if level in self.refs:
            arrayUse = self.refs[level]
            arrayUse.extend(refsInLevel)
            self.refs[level]=arrayUse
        else:
            self.refs[level] = refsInLevel
        
            

    def parserRef(sefl, response):
        refsInLevel = []
        arrayUse = []
        hxs = HtmlXPathSelector(response)
        refs = hxs.select('//div[@id="citations"]/table/tr')
        level = response.meta['level']
        self = response.meta['self']
        levelUse = int(level)
        if levelUse < 3:
            for ref in refs:
                refTitle = ref.select('td/a/text()').extract()[0]
                refUrl = ref.select('td/a/@href').extract()[0]
                refDic = {"title":refTitle, "url":refUrl}
                refsInLevel.append(refDic)
            if level in self.refs:
                arrayUse = self.refs[level]
                arrayUse.extend(refsInLevel)
                self.refs[level]=arrayUse
            else:
                self.refs[level] = refsInLevel
            for ref in self.refs[level]:
                levelNext = str(levelUse+1)
                yield Request(url = "http://citeseerx.ist.psu.edu"+ref['url'], meta = {"level":levelNext, "self":self},callback = self.parserRef)
        else:
            yield self.extractData()
        
        

    def parser_cite(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="result"]')
        self.cites.extend(self.parse_citeTitle(sites))
        urlNext = hxs.select('//div[@id="pager"]/a/@href').extract()
        if urlNext:
            urlNext = "http://citeseerx.ist.psu.edu"+urlNext[0]
            checkRequest = Request(
                url = urlNext,
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


    def extractData(self):
        paper = CiteseerPaperItem()
        paper['_id'] = self._id
        paper['title'] = self.title
        paper['abstart'] = self.abs
        paper['defpaper'] = self.refs
        paper['citebypaper'] = self.cites
        return paper
    
