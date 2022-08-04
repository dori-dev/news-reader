from django.contrib import admin
from django.utils.html import format_html
from .models import New


class NewAdmin(admin.ModelAdmin):
    list_display = (
        "title", "pub_date", "url",
        "image", "tags"
    )
    list_filter = ("categories",)
    search_fields = ("title", "description")

    def url(self, model: New):
        link = model.link
        return format_html(f'<a target="_blank" href="{link}">Link</a>')

    def image(self, model: New):
        image_url = model.thumbnail
        return format_html(f'<a target="_blank" href="{image_url}">Image</a>')

    def tags(self, model: New):
        return list(model.categories.all())


admin.site.register(New, NewAdmin)
