# Scrapy settings for citeSeer project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'citeSeer'

SPIDER_MODULES = ['citeSeer.spiders']
NEWSPIDER_MODULE = 'citeSeer.spiders'

DEFAULT_ITEM_CLASS = 'citeSeer.items.CiteseerItem'
# ITEM_PIPELINES = ['citeSeer.pipelines.CiteseerPipeline']
ITEM_PIPELINES = {"citeSeer.pipelines.MongoDBPipeline": 300, "citeSeer.pipelines.JsonWriterPipeline": 800}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "test"
MONGODB_COLLECTION = "show"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'citeSeer (+http://www.yourdomain.com)'
