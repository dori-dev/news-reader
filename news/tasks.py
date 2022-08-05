from celery import shared_task
from .models import New
from . import scraper

rss_urls = [
    "https://www.isna.ir/rss",
    "https://www.khabaronline.ir/rss",
    "https://www.mehrnews.com/rss",
]


@shared_task()
def get_latest_news():
    data = scraper.get_data(rss_urls)
    for new in data:
        search_new = New.objects.filter(title=new.title.strip())
        if not search_new.exists():
            try:
                New.create_new(new)
            except Exception:
                pass
