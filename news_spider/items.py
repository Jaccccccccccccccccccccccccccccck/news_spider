import scrapy


class NewsItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    content = scrapy.Field()
    rich_content = scrapy.Field()
    referer = scrapy.Field()
