from django.conf import settings
from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RangeDateFilter, RelatedDropdownFilter
from unfold.decorators import action, display

from .models import Category, Post, Tag


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["title_with_emoji", "slug", "posts_count", "order"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_count=Count("posts"))

    @display(description="Mavzu", ordering="name")
    def title_with_emoji(self, obj):
        return f"{obj.emoji} {obj.name}".strip()

    @display(description="Maqolalar", ordering="_count")
    def posts_count(self, obj):
        return obj._count


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ["name", "slug", "posts_count"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_count=Count("posts"))

    @display(description="Maqolalar", ordering="_count")
    def posts_count(self, obj):
        return obj._count


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ["post", "category", "status_label", "published_at", "views", "reading_time", "is_featured"]
    list_editable = ["is_featured"]
    list_filter = [
        ("status", ChoicesDropdownFilter),
        ("category", RelatedDropdownFilter),
        ("published_at", RangeDateFilter),
        "is_featured",
    ]
    list_filter_submit = True
    search_fields = ["title", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["tags"]
    date_hierarchy = "published_at"
    save_on_top = True
    actions = ["publish_now", "make_draft"]
    readonly_fields = ["views", "reading_time"]
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "category", "tags", "cover", "excerpt"),
        }),
        ("Matn", {
            "fields": ("content",),
        }),
        ("Chop etish", {
            "fields": ("status", "published_at", "is_featured", "views", "reading_time"),
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description"),
            "classes": ["collapse"],
        }),
    )

    @display(description="Maqola", header=True)
    def post(self, obj):
        cover = {"path": obj.cover.url, "squared": True, "width": 64, "height": 40} if obj.cover else None
        return [obj.title, obj.excerpt[:80] if obj.excerpt else "", "✍", cover]

    @display(description="Holat", label={"Qoralama": "warning", "Chop etilgan": "success"})
    def status_label(self, obj):
        return obj.get_status_display()

    @action(description="Hozir chop etish")
    def publish_now(self, request, queryset):
        queryset.update(status=Post.Status.PUBLISHED, published_at=timezone.now())

    @action(description="Qoralamaga qaytarish")
    def make_draft(self, request, queryset):
        queryset.update(status=Post.Status.DRAFT)

    def view_on_site(self, obj):
        return f"{settings.FRONTEND_URL}/blog/{obj.slug}"
