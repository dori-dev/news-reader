from django.shortcuts import render
from .models import New
from . import scraper


rss_urls = [
    "https://www.isna.ir/rss",
]


def index(request):
    data = scraper.get_data(rss_urls)
    for new in data:
        New.create_new(new)
    context = {
        'news': data
    }
    return render(request, 'news/index.html', context)
