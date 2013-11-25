from scrapy.item import Item, Field

class CiteseerItem(Item):
    title = Field()
    url = Field()

class CiteseerPaperItem(Item):
    _id = Field() #10.x.x...
    title = Field() #paper title
    abstart = Field() #paper abstart
    url = Field() #paper url
    defpaper = Field() #put ref paper id
    citebypaper = Field() #put cite paper id