import json
import os

import scrapy
import validators
from scrapy import signals
from scrapy.linkextractors import LinkExtractor

from news_spider.news_config import news_configs
from news_spider.news_parser import news_parser


class NewsRankSpider(scrapy.Spider):
    name = "news_spider"

    def __init__(self, *args, **kwargs):
        super(NewsRankSpider, self).__init__(*args, **kwargs)
        self.source = kwargs.get('source')
        news_rank_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../news_out/news_rank.json")
        news_rank_file = open(news_rank_path, 'r', encoding='utf-8')
        self.news_rank = json.load(news_rank_file)

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(NewsRankSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    #     return spider

    def start_requests(self):
        if self.source:
            news_config = news_configs[self.source]
            for news_list_url, rank in self.news_rank.get(self.source).items():
                if rank < 10:
                    continue
                yield scrapy.Request(
                    url=news_list_url,
                    headers={
                        'Referer': news_config['base_url']
                    },
                    meta={
                        'news_config': news_config
                    }
                )
        else:
            for source, source_rank_list in self.news_rank.items():
                news_config = news_configs[source]
                for news_list_url, rank in source_rank_list.items():
                    yield scrapy.Request(
                        url=news_list_url,
                        headers={
                            'Referer': news_config['base_url']
                        },
                        meta={
                            'news_config': news_config
                        }
                    )

    def parse(self, response):
        meta = response.meta
        news_config = meta['news_config']
        is_news, news_item = news_parser(news_config, response)
        referer = response.request.headers.get('Referer')
        if not referer:
            return
        referer = referer.decode('utf-8')
        if is_news:
            news_item['url'] = response.url
            news_item['referer'] = referer
            yield news_item
        else:
            pass
        # follow pages
        if meta['depth'] >= 1:
            return
        for link in LinkExtractor(allow_domains=news_config['allow_domains']).extract_links(response):
            if validators.url(link.url):
                yield scrapy.Request(
                    url=link.url,
                    meta={
                        'news_config': news_config
                    }
                )

    # def spider_closed(self, spider):
    #     news_rank_out_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../news_out/news_rank.json")
    #
    #     with open(news_rank_out_path, 'w') as rank_result:
    #         rank_result.write(json.dumps(self.news_rank, indent=2))
    #     spider.logger.info(f'Spider closed: {spider.name}')
