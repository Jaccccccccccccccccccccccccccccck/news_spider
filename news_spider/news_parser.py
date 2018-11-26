import re

import lxml
from lxml.html.clean import Cleaner
from scrapy.http import Response

from news_spider.items import NewsItem


def remove_space(_str):
    if _str:
        return re.sub(r'\s', '', _str)
    else:
        return None


def _extract(extractors, response):
    if not extractors or not response:
        return None
    if extractors and not hasattr(extractors, '__iter__'):
        extractors = [extractors]
    for extractor in extractors:
        ret = extractor(response)
        if ret:
            return ret
    return None


class FieldExtractor(object):

    def __init__(self):
        super(FieldExtractor, self).__init__()

    def __call__(self, response):
        pass


class XPath(FieldExtractor):

    def __init__(self, xpath, *processors, **kwargs):
        super(XPath, self).__init__()
        self.xpath = xpath
        self.processors = processors

    def __call__(self, response):
        value = response.xpath(self.xpath)
        for processor in self.processors:
            if value:
                value = processor(value)
            else:
                return None
        return value


class XPathFirst(FieldExtractor):

    def __init__(self, xpath, *processors, **kwargs):
        super(XPathFirst, self).__init__()
        self.xpath = xpath
        self.processors = processors

    def __call__(self, response):
        value = response.xpath(self.xpath).extract_first()
        for processor in self.processors:
            if value:
                try:
                    value = processor(value)
                except:
                    return
            else:
                return None
        return value


def clean_html_content_text(html_str):
    cleaner = Cleaner()
    cleaner.javascript = True  # This is True because we want to activate the javascript filter
    cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter

    cleaned_html = cleaner.clean_html(lxml.html.fromstring(html_str))
    cleaned_content = lxml.html.tostring(cleaned_html, encoding='utf-8').decode()

    return cleaned_html, cleaned_content


def news_parser(news_config: dict, response: Response):
    title = _extract([XPathFirst(xpath_str) for xpath_str in news_config['title_xpath_list']], response)
    author = _extract([XPathFirst(xpath_str) for xpath_str in news_config['author_xpath_list']], response)
    publish_time = _extract([XPathFirst(xpath_str) for xpath_str in news_config['publish_time_xpath_list']], response)
    rich_content_origin = _extract([XPathFirst(xpath_str) for xpath_str in news_config['content_xpath_list']], response)
    cleaned_content, cleaned_content_text = clean_html_content_text(rich_content_origin)

    return NewsItem(
        source=news_config['source'],
        title=title,
        author=author,
        publish_time=publish_time,
        content=cleaned_content_text,
        rich_content=cleaned_content,
    )
