BOT_NAME = 'PhpBbThreadToPdfBot'

SPIDER_MODULES = ['CrawlPhpBbThread.spiders']
NEWSPIDER_MODULE = 'CrawlPhpBbThread.spiders'

USER_AGENT = 'PhpBbThreadToPdfBot'
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'CrawlPhpBbThread.pipelines.CrawlPhpBbForumPipeline': 300,
}

LOG_LEVEL = 'ERROR'