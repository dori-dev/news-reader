from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from taggit.models import Tag
from .models import New


class NewsIndex(ListView):
    model = New
    paginate_by = 8
    context_object_name = 'news'
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Tag.objects.filter(
                show_tag=True
            ).exclude(
                showing=False
            ).order_by('name'),
            'label': 'آخرین اخبار'
        })
        return context

    def get_queryset(self):
        return New.objects.exclude(
            categories__showing=False
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
            'categories': Tag.objects.filter(
                show_tag=True
            ).exclude(
                showing=False
            ).order_by('name'),
            'label': tag_object.name
        })
        return context

    def get_queryset(self):
        tag = self.kwargs['tag']
        tag_object = get_object_or_404(Tag, slug=tag)
        return New.objects.filter(
            categories__slug=tag_object.slug
        ).exclude(
            categories__showing=False
        ).order_by('-pub_date')
