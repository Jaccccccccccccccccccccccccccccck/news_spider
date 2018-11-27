news_configs = {
    "sina": {
        'source': 'sina',
        'base_url': 'http://finance.sina.com.cn',
        'title_xpath_list': ['//meta[@property="og:title"]/@content'],
        'author_xpath_list': ['//*[@class ="source ent-source"]/text()'],
        'publish_time_xpath_list': ['//meta[@property="article:published_time"]/@content'],
        'content_xpath_list': ['id("artibody")', 'id("articleContent")'],
        'allow_domains': ("finance.sina.com.cn",),
    },
}
