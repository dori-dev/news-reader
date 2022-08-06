from typing import List
from requests import get, exceptions
from .rss_parser import Parser, FeedItem


TIMEOUT = 2


def get_data(rss_urls: list) -> List[FeedItem]:
    result = []
    for rss_url in rss_urls:
        try:
            xml = get(rss_url, timeout=TIMEOUT)
        except (exceptions.ConnectionError, exceptions.ReadTimeout):
            continue
        try:
            parser = Parser(xml.content.decode('utf-8', 'ignore'))
            feed = parser.parse()
            data = feed.feed
            result.extend(data)
        except Exception:
            pass
    return result
