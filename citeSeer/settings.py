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

# DEFAULT_ITEM_CLASS = ['citeSeer.items.CiteseerItem', 'citeSeer.items.CiteseerPaperItem']
# ITEM_PIPELINES = ['citeSeer.pipelines.MongoDBPipeline']
# ITEM_PIPELINES = {"citeSeer.pipelines.MongoDBPipeline": 300, "citeSeer.pipelines.JsonWriterPipeline": 800}
ITEM_PIPELINES = {"citeSeer.pipelines.MongoDBPipeline": 300}
# DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "test"
MONGODB_COLLECTION = "ieeeData"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'citeSeer (+http://www.yourdomain.com)'

SENTRY_DSN = 'http://2954d89b62b94cb984787f8ca489946d:ff063d4894034af99c6928903e990bf6@localhost:9000/2'
EXTENSIONS = {
  "scrapy_sentry.extensions.Errors":10,
}