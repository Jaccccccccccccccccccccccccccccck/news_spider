import json
import os

import scrapy
import validators
from scrapy import signals
from scrapy.linkextractors import LinkExtractor

from news_spider.news_config import news_configs
from news_spider.news_parser import news_parser


class NewsRankSpider(scrapy.Spider):
    name = "news_rank_spider"

    def __init__(self, *args, **kwargs):
        super(NewsRankSpider, self).__init__(*args, **kwargs)
        self.source = kwargs.get('source')
        self.news_rank = dict()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(NewsRankSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def start_requests(self):
        if self.source:
            news_config = news_configs[self.source]
            yield scrapy.Request(
                url=news_config['base_url'],
                headers={
                    'Referer': news_config['base_url']
                },
                meta={
                    'news_config': news_config
                }
            )
            self.news_rank[self.source] = {}
        else:
            for source, news_config in news_configs.items():
                yield scrapy.Request(
                    url=news_config['base_url'],
                    headers={
                        'Referer': news_config['base_url']
                    },
                    meta={
                        'news_config': news_config
                    }
                )
                self.news_rank[source] = {}

    def parse(self, response):
        meta = response.meta
        news_config = meta['news_config']
        source = news_config['source']
        is_news, news_item = news_parser(news_config, response)
        if is_news:
            referer_url = response.request.headers.get('Referer', None)
            if referer_url:  # todo: why referer is None ?
                if isinstance(referer_url, bytes):
                    referer_url = referer_url.decode('utf-8')
                if self.news_rank[source].get(referer_url):
                    self.news_rank[source][referer_url] = self.news_rank[source][referer_url] + 1
                else:
                    self.news_rank[source][referer_url] = 1
        else:
            pass
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

    def spider_closed(self, spider):
        news_rank_out_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../news_out/news_rank.json")

        with open(news_rank_out_path, 'w') as rank_result:
            rank_result.write(json.dumps(self.news_rank, indent=2))
        spider.logger.info(f'Spider closed: {spider.name}')
