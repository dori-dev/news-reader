from datetime import datetime, timedelta
from typing import Any
from django.db import models
from django.utils.timezone import make_aware, now
from taggit.managers import TaggableManager
from .rss_parser import FeedItem

GMP_IRAN_TIMEZONE = timedelta(hours=4, minutes=30)


class New(models.Model):
    title = models.CharField(
        max_length=256
    )
    pub_date = models.DateTimeField()
    link = models.URLField()
    thumbnail = models.URLField()
    description = models.TextField()
    categories = TaggableManager()

    @staticmethod
    def create_new(new_item: FeedItem):
        title = new_item.title
        # extract and set published date
        pub_date = New.convert_date(new_item.pub_date)
        link = new_item.link
        thumbnail = new_item.thumbnail
        description = new_item.description
        # create object
        new: New = New.objects.create(
            title=title,
            pub_date=pub_date,
            link=link,
            thumbnail=thumbnail,
            description=description
        )
        # add categories
        categories = New.set_categories(new_item.categories)
        if categories:
            new.categories.add(*categories)
        new.save()

    @staticmethod
    def convert_date(date: str) -> datetime:
        # sample date: Fri, 05 Aug 2022 06:45:15 GMT
        try:
            pub_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            return now()
        pub_date = pub_date + GMP_IRAN_TIMEZONE
        pub_date = make_aware(pub_date)
        return pub_date

    @staticmethod
    def set_categories(categories: str) -> Any:
        if ">" in categories:
            sep = ">"
        elif " و " in categories:
            sep = " و "
        else:
            sep = None
        if sep is not None:
            categories = list(map(
                str.strip,
                categories.split(sep)
            ))
        return categories

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
