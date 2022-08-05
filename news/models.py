from datetime import datetime, timedelta
from typing import List
from django.db import models
from django.utils.timezone import make_aware
from taggit.managers import TaggableManager

IRAN_TIMEZONE = timedelta(hours=4, minutes=30)


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
    def create_new(item: dict):
        title = item["title"]
        pub_date = New.convert_date(item["pubDate"])
        # extract link
        link = item["link"]
        if not link:
            link = item["guid"]
        # extract thumbnail
        enclosure = item["enclosure"]
        if enclosure:
            thumbnail = enclosure['link']
        else:
            thumbnail = item["thumbnail"]
        # extract description
        description = item["description"]
        if not description:
            description = item["content"]
        # create object
        new: New = New.objects.create(
            title=title,
            pub_date=pub_date,
            link=link,
            thumbnail=thumbnail,
            description=description
        )
        # add categories
        categories: List[str] = item["categories"]
        if categories:
            categories = list(map(
                str.strip,
                categories[0].split("&gt;")
            ))
            new.categories.add(*categories)
        new.save()

    @staticmethod
    def convert_date(date: str) -> datetime:
        pub_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        pub_date = pub_date + IRAN_TIMEZONE
        pub_date = make_aware(pub_date)
        return pub_date

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
