from datetime import datetime, timedelta
from django.db import models
from django.utils.timezone import make_aware, now
from taggit.managers import TaggableManager
from .rss_parser import FeedItem

GMP_IRAN_TIMEZONE = timedelta(hours=4, minutes=30)


class New(models.Model):
    title = models.CharField(
        max_length=256,
        unique=True
    )
    pub_date = models.DateTimeField()
    link = models.URLField(
        unique=True
    )
    thumbnail = models.URLField(
        unique=True
    )
    description = models.TextField()
    categories = TaggableManager()

    @staticmethod
    def create_new(new_item: FeedItem):
        title = new_item.title.strip()
        # extract and set published date
        pub_date = New.convert_date(new_item.pub_date)
        link = new_item.link.strip()
        thumbnail = new_item.thumbnail.strip()
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
        categories = New.set_categories(
            New.replace_category(new_item.categories)
        )
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
    def set_categories(categories: str) -> list:
        not_allowed_char = "،"
        if ">" in categories:
            sep = ">"
        elif " و " in categories:
            sep = " و "
        else:
            sep = None
        if sep is not None:
            return list(filter(
                lambda category: not_allowed_char not in category,
                map(
                    str.strip,
                    categories.split(sep)
                )
            ))
        return [categories]

    @staticmethod
    def replace_category(input_categories: str):
        replaces = {
            ("اخبار استان ها", "استانها"): "استان‌ها",
            ("سایر ورزشها", "جهان ورزش", "دیگر ورزش‌ها", "ورزشی"): "ورزش",
            ("فوتبال ملی"): "فوتبال ایران",
        }
        for categories in replaces.keys():
            for category in categories:
                input_categories = input_categories.replace(
                    category,
                    replaces[categories]
                )
        return input_categories

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
