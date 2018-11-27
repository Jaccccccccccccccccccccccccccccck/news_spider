# news_spider
1.How to run:

    scrapy crawl news_rank_spider [-a source=sina]  # output will be in news_spider/news_out/news_rank.json

    scrapy crawl news_spider [-a source=sina] -o news_spider/news_out/news.json  # output will be in news_spider/news_out/news.json 

2.How to add news source

    modify file: news_spider/news_config.py
