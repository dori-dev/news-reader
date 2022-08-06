from celery import shared_task
from .models import New
from . import scraper

rss_urls = [
    "https://www.isna.ir/rss",
    "https://www.khabaronline.ir/rss",
    "https://www.mehrnews.com/rss",
    "https://www.mashreghnews.ir/rss",
    "https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B1%D9%88%D8%B2",
    "https://www.tasnimnews.com/fa/rss/feed/0/7/3/%D9%88%D8%B1%D8%B2%D8%B4%DB%8C?hit=1",
]


@shared_task()
def get_latest_news():
    try:
        data = scraper.get_data(rss_urls)
    except Exception:
        return
    for new in data:
        search_new = New.objects.filter(title=new.title.strip())
        if not search_new.exists():
            try:
                New.create_new(new)
            except Exception:
                pass
