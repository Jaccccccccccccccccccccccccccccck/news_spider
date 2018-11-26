import scrapy
import validators
from scrapy.linkextractors import LinkExtractor

from news_spider.news_config import news_configs
from news_spider.news_parser import news_parser


class NewsRankSpider(scrapy.Spider):
    name = "news_rank_spider"

    def __init__(self, *args, **kwargs):
        super(NewsRankSpider, self).__init__(*args, **kwargs)
        self.source = kwargs.get('source')
        self.news_rank = {}

    def start_requests(self):
        if self.source:
            news_config = news_configs[self.source]
            yield scrapy.Request(
                url=news_config['base_url'],
                headers={
                    'referer': news_config['base_url']
                },
                meta={
                    'news_config': news_config
                }
            )
        else:
            for source, news_config in news_configs.items():
                yield scrapy.Request(
                    url=news_config['base_url'],
                    headers={
                        'referer': news_config['base_url']
                    },
                    meta={
                        'news_config': news_config
                    }
                )

    def parse(self, response):
        meta = response.meta
        news_config = meta['news_config']
        news_item = news_parser(news_config, response)

        if news_item.get('title') and news_item.get('publish_time') and news_item.get('content'):
            self.logger.debug(f'[IS NEWS]<title>:{news_item["title"]}, '
                              f'<publish_time>:{news_item["publish_time"]}'
                              f'<content_text>:{news_item["content"]}')
        else:
            self.logger.debug(f'[NOT NEWS]:{response.url}')
        # follow pages
        if meta['depth'] >= 2:
            return
        for link in LinkExtractor(allow_domains=news_config['allow_domains']).extract_links(response):
            if validators.url(link.url):
                yield scrapy.Request(
                    url=link.url,
                    meta={
                        'news_config': news_config
                    }
                )
