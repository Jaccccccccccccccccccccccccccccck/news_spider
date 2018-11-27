# news_spider
1.How to run:

    >>> scrapy crawl news_rank_spider [-a source=sina]  # output will be in news_spider/news_out/news_rank.json

    >>> scrapy crawl news_spider [-a source=sina] -o news_spider/news_out/news.json  # output will be in news_spider/news_out/news.json 

2.How to add news source

    modify file: news_spider/news_config.py

3.What does news source config detail mean:
       
    news_configs = {
        "sina": {  # source name
            'source': 'sina',  # same as above
            'base_url': 'http://finance.sina.com.cn',  # website base url
            'title_xpath_list': ['//meta[@property="og:title"]/@content'],  # xpath to get title. why list? see 4
            'author_xpath_list': ['//*[@class ="source ent-source"]/text()'],  # xpath to get author
            'publish_time_xpath_list': ['//meta[@property="article:published_time"]/@content'], # xpath to get publish time
            'content_xpath_list': ['id("artibody")', 'id("articleContent")'],  # xpath to get main content
            'allow_domains': ("finance.sina.com.cn",),  # allow domains when extract follow pages
        },
        "***":{  # new source
            'source': *,
            'base_url': *,
            'title_xpath_list': [*,],
            'author_xpath_list': [*,],
            'publish_time_xpath_list': [*,],
            'content_xpath_list': [*,],
            'allow_domains': (*,),
        }
    }

4.Why xpath list:

    Website may use different xpath in different column. Add as many xpath as you can find, otherwise you will miss some news.

5.TODO:

    1.[TODO]Output publish time as datetime formated str, now origin str
    
