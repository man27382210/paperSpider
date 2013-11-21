from scrapy.item import Item, Field

class CiteseerItem(Item):
    title = Field()
    url = Field()
