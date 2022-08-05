from typing import List
from requests import get, exceptions
from .rss_parser import Parser, FeedItem


TIMEOUT = 2

# should get from admin site and database(with default)
rss_urls = {
    "home": {
        "isna": "https://www.isna.ir/rss-homepage",
        "mehrnews": "https://www.mehrnews.com/rss-homepage",
    },
    "latest": {
        "khabaronline": "https://www.khabaronline.ir/rss",
        "mehrnews": "https://www.mehrnews.com/rss",
        "mashreghnews": "https://www.mashreghnews.ir/rss",
        "isna": "https://www.isna.ir/rss",
        "tasnimnews": "https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B1%D9%88%D8%B2",
    },
    "sport": {
        # TODO varzesh3 not have category
        "latest": "https://www.varzesh3.com/rss/all",
        "local_football": "https://www.varzesh3.com/rss/domesticfootball",
        "foreign_football": "https://www.varzesh3.com/rss/foreignfootball",
        "tasnimnews": "https://www.tasnimnews.com/fa/rss/feed/0/7/3/%D9%88%D8%B1%D8%B2%D8%B4%DB%8C?hit=1"
    },
    "other": {
        "most_viewed": "https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D9%BE%D8%B1%D8%A8%DB%8C%D9%86%D9%86%D8%AF%D9%87-%D8%AA%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1?hit=1",
        "most_important": "https://www.tasnimnews.com/fa/rss/feed/0/8/0/%D9%85%D9%87%D9%85%D8%AA%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1",
        "selected_news": "https://www.tasnimnews.com/fa/rss/feed/0/9/0/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A8%D8%B1%DA%AF%D8%B2%DB%8C%D8%AF%D9%87"
    }
}


def get_data(rss_urls: list) -> List[FeedItem]:
    result = []
    for rss_url in rss_urls:
        try:
            xml = get(rss_url, timeout=TIMEOUT)
        except (exceptions.ConnectionError, exceptions.ReadTimeout):
            continue
        parser = Parser(xml.content)
        feed = parser.parse()
        data = feed.feed
        result.extend(data)
    return result
