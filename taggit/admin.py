from django.contrib import admin

from taggit.models import Tag, TaggedItem


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


@admin.action(description="Showing selected tags")
def set_showing_true(modeladmin, request, queryset):
    queryset.update(showing=True)


@admin.action(description="Not showing selected tags")
def set_showing_false(modeladmin, request, queryset):
    queryset.update(showing=False)


@admin.action(description="Show tag label, selected tags")
def set_show_tag_true(modeladmin, request, queryset):
    queryset.update(show_tag=True)


@admin.action(description="Not show tag label, selected tags")
def set_show_tag_false(modeladmin, request, queryset):
    queryset.update(show_tag=False)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug", "show_tag", "showing"]
    list_filter = ["showing", "show_tag"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    actions = [set_showing_true, set_showing_false,
               set_show_tag_true, set_show_tag_false]
