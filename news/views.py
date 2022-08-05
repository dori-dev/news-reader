from django.shortcuts import render
from taggit.models import Tag
from .models import New
from . import scraper


rss_urls = [
    "https://www.isna.ir/rss",
    "https://www.khabaronline.ir/rss",
    "https://www.mehrnews.com/rss",
]


def index(request):
    data = scraper.get_data(rss_urls)
    for new in data:
        search_new = New.objects.filter(title=new.title)
        if not search_new.exists():
            New.create_new(new)
    context = {
        'news': New.objects.order_by('-pub_date'),
        'tags': Tag.objects.all()
    }
    return render(request, 'news/index.html', context)
