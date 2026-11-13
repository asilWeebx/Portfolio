from django.conf import settings
from django.contrib import admin
from django.db.models import Count
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RelatedDropdownFilter
from unfold.decorators import display

from .models import Project, ProjectCategory, ProjectImage


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1
    fields = ["image", "caption", "order"]
    tab = True


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(ModelAdmin):
    list_display = ["name", "slug", "projects_count", "order", "is_active"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_count=Count("projects"))

    @display(description="Loyihalar", ordering="_count")
    def projects_count(self, obj):
        return obj._count


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ["project", "category", "year", "is_featured", "is_published", "order"]
    list_editable = ["is_featured", "is_published", "order"]
    list_filter = [("category", RelatedDropdownFilter), "is_featured", "is_published", "year"]
    list_filter_submit = True
    search_fields = ["title", "short_description", "client"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["technologies"]
    inlines = [ProjectImageInline]
    save_on_top = True
    fieldsets = (
        ("Asosiy", {
            "fields": ("title", "slug", "category", "short_description", "cover", "logo", "accent_color"),
        }),
        ("Case study (batafsil)", {
            "fields": ("content",),
            "classes": ["tab"],
        }),
        ("Tafsilotlar", {
            "fields": ("client", "role", "year", "duration", "technologies"),
            "classes": ["tab"],
        }),
        ("Havolalar", {
            "fields": ("live_url", "play_store_url", "app_store_url", "desktop_url", "has_desktop", "telegram_url", "github_url"),
            "classes": ["tab"],
        }),
        ("Ko'rinish va SEO", {
            "fields": ("is_published", "is_featured", "order", "seo_title", "seo_description"),
            "classes": ["tab"],
        }),
    )

    @display(description="Loyiha", header=True)
    def project(self, obj):
        cover = {"path": obj.cover.url, "squared": True, "width": 64, "height": 40} if obj.cover else None
        return [obj.title, obj.short_description[:70], obj.title[:2].upper(), cover]

    def view_on_site(self, obj):
        return f"{settings.FRONTEND_URL}/portfolio/{obj.slug}"
