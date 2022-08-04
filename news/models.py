from datetime import datetime
from typing import List
from django.db import models
from django.utils.timezone import make_aware
from taggit.managers import TaggableManager


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
        pub_date = item["pubDate"]
        link = item["link"]
        if not link:
            link = item["guid"]
        enclosure = item["enclosure"]
        if enclosure:
            thumbnail = enclosure['link']
        else:
            thumbnail = item["thumbnail"]
        description = item["description"]
        if not description:
            description = item["content"]
        categories: List[str] = item["categories"]
        pub_date = datetime.strptime(pub_date, "%Y-%m-%d %H:%M:%S")
        pub_date = make_aware(pub_date)
        new: New = New.objects.create(
            title=title,
            pub_date=pub_date,
            link=link,
            thumbnail=thumbnail,
            description=description
        )
        if categories:
            categories = list(map(
                str.strip,
                categories[0].split("&gt;")
            ))
            new.categories.add(*categories)
        new.save()

    def __str__(self):
        return self.title
