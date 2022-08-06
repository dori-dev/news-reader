from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from taggit.models import Tag
from .models import New

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


class NewsIndex(ListView):
    model = New
    paginate_by = 8
    context_object_name = 'news'
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Tag.objects.exclude(
                name__in=not_allowed_categories
            ).order_by('name'),
            'label': 'آخرین اخبار'
        })
        return context

    def get_queryset(self):
        return New.objects.filter(
            pub_date__lt=timezone.now()
        ).order_by('-pub_date')


class Category(ListView):
    model = New
    paginate_by = 8
    context_object_name = 'news'
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs['tag']
        tag_object = get_object_or_404(Tag, slug=tag)
        context.update({
            'categories': Tag.objects.exclude(
                name__in=not_allowed_categories
            ).order_by('name'),
            'label': tag_object.name
        })
        return context

    def get_queryset(self):
        tag = self.kwargs['tag']
        tag_object = get_object_or_404(Tag, slug=tag)
        return New.objects.filter(
            categories__slug=tag_object.slug,
            pub_date__lt=timezone.now()
        ).order_by('-pub_date')
