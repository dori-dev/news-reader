import json
import requests
from requests import exceptions
from all_rss import rss_urls
from api_key import api_key

API = "https://api.rss2json.com/v1/api.json"
api_data = {
    'rss_url': '',
    'api_key': api_key,
    'count': 50,
}
TIMEOUT = 2


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
