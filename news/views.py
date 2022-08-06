from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from taggit.models import Tag
from .models import New
from .tasks import get_latest_news

not_allowed_categories = [
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
        'categories': Tag.objects.exclude(name__in=not_allowed_categories),
        'label': 'آخرین اخبار'
    }
    return render(request, 'news/news.html', context)


def category(request, tag: str):
    tag_object = get_object_or_404(Tag, slug=tag)
    try:
        get_latest_news.apply_async()
    except Exception:
        pass
    context = {
        'news': New.objects.filter(
            categories__slug=tag,
            pub_date__lt=timezone.now()
        ).order_by('-pub_date')[:20],
        'categories': Tag.objects.exclude(name__in=not_allowed_categories),
        'label': tag_object.name
    }
    return render(request, 'news/news.html', context)
