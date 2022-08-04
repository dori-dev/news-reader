import json
import requests
from requests import exceptions
from django.conf import settings

API = "https://api.rss2json.com/v1/api.json"
api_data = {
    'rss_url': '',
    'api_key': settings.API_KEY,
    'count': 50,
}
TIMEOUT = 2
# should get from admin site and database(with default)
rss_urls = {
    "home": {
        "isna": "https://www.isna.ir/rss-homepage",
        "mehrnews": "https://www.mehrnews.com/rss-homepage",
        "entekhab": "https://www.entekhab.ir/fa/rss/1",
    },
    "latest": {
        "khabaronline": "https://www.khabaronline.ir/rss",
        "mehrnews": "https://www.mehrnews.com/rss",
        "mashreghnews": "https://www.mashreghnews.ir/rss",
        "entekhab": "https://www.entekhab.ir/fa/rss/allnews",
        "isna": "https://www.isna.ir/rss",
        "tasnimnews": "https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B1%D9%88%D8%B2",
    },
    "sport": {
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


def extract_data(item: dict):
    title = item["title"]
    pubDate = item["pubDate"]
    link = item["link"]
    guid = item["guid"]
    author = item["author"]
    thumbnail = item["thumbnail"]
    description = item["description"]
    content = item["content"]
    enclosure: dict = item["enclosure"]
    categories: list = item["categories"]
    return (
        title, pubDate, link, guid,
        author, thumbnail, description,
        content, enclosure, categories
    )


count = 0
for rss_url in rss_urls:
    api_data['rss_url'] = rss_url
    try:
        response = requests.post(
            API,
            data=api_data,
            timeout=TIMEOUT
        )
    except (exceptions.ConnectionError, exceptions.ReadTimeout):
        continue
    data = json.loads(response.text)
    items = data['items']
    for item in items:
        count += 1
        try:
            the_item = extract_data(item)
        except KeyError:
            continue
        else:
            pass
            # print(the_item)

print(count)
