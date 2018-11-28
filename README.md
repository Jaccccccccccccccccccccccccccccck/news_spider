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

5.Why news rank spider + news spider instead of news spider
    
    This is how I see about news website, all pages can be treated as follows
	1.list pages(column pages)
		https://xueqiu.com/ (base url)
		https://xueqiu.com/#/cn
		https://xueqiu.com/#/hk
		https://xueqiu.com/#/**
	2.news pages
		https://xueqiu.com/7290870926/116963535
		https://xueqiu.com/4489918820/116945915
		https://xueqiu.com/***/***
	3.junk pages
		https://broker.xueqiu.com/
		https://xueqiu.com/ask/square
		https://xueqiu.com/people
		***
			
    Easy to add source: 
        Add a news source by adding a dict(with base url only)
    Auto detect news column pages: 
        News rank spider(depth<=2) just run once for news rank result, and pages with high rank are list pages normally. 
    Less request when crawl news: 
        News spider(depth<=1) crawl selected list pages.
    Flexible:
        Choose list pages you want to start news spider by modify news_rank.json


6.TODO:

    1.[TODO] Output publish time as datetime formated str, now origin str
    2.[TODO] Support request with js render
    3.[TODO] Collect not page set in news rank spider and use in news spider
    4.[TODO] A nicer GUI for add news source
    5.[TODO] A nicer GUI(or something) for modify rank list result
    6.[TODO] Adjust concurrency
    7.[TODO] Request with proxy
