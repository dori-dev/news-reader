from django.shortcuts import render
from django.utils import timezone
from taggit.models import Tag
from .models import New
from .tasks import get_latest_news

not_allowed_tags = [
    "تهران",
    "خراسان رضوی",
    "اصفهان",
    "فارس",
    "خوزستان",
    "آذربایجان شرقی",
    "مازندران",
    "آذربایجان غربی",
    "کرمان",
    "سیستان و بلوچستان",
    "البرز",
    "گیلان",
    "کرمانشاه",
    "گلستان",
    "هرمزگان",
    "لرستان",
    "همدان",
    "کردستان",
    "مرکزی",
    "قم",
    "قزوین",
    "اردبیل",
    "بوشهر",
    "یزد",
    "زنجان",
    "چهارمحال و بختیاری",
    "خراسان شمالی",
    "خراسان جنوبی",
    "کهگیلویه و بویراحمد",
    "سمنان",
    "ایلام",
]


def index(request):
    try:
        get_latest_news.apply_async()
    except Exception:
        pass
    context = {
        'news': New.objects.filter(
            pub_date__lt=timezone.now()
        ).order_by('-pub_date')[:20],
        'tags': Tag.objects.exclude(name__in=not_allowed_tags)
    }
    return render(request, 'news/index.html', context)
