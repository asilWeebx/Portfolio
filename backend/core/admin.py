from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RangeDateFilter
from unfold.decorators import action, display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import (
    Client, ContactRequest, Experience, Service, SiteSettings, Technology, Testimonial,
)

# Standart User/Group admin'ini Unfold uslubiga o'tkazamiz
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


def thumb(url: str | None, size: int = 40, rounded: bool = False) -> dict | None:
    if not url:
        return None
    return {"path": url, "squared": not rounded, "width": size, "height": size}


# --------------------------------------------------------------------------- Sayt sozlamalari
@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ("Hero (birinchi ekran)", {
            "fields": ("full_name", "role", "hero_title", "hero_subtitle", "available_for_work"),
        }),
        ("Men haqimda", {
            "fields": ("about_title", "about_text", "avatar", "about_photo", "cv_file"),
        }),
        ("Raqamlar", {
            "fields": ("years_experience", "happy_clients"),
            "description": "Loyihalar soni avtomatik hisoblanadi.",
        }),
        ("Kontaktlar", {
            "fields": ("phone", "email", "location", "telegram", "github", "linkedin", "instagram", "youtube"),
        }),
        ("SEO", {
            "fields": ("meta_description", "og_image"),
            "classes": ["tab"],
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return HttpResponseRedirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))


# --------------------------------------------------------------------------- Texnologiyalar
@admin.register(Technology)
class TechnologyAdmin(ModelAdmin):
    list_display = ["tech", "group", "show_on_home", "order", "is_active"]
    list_editable = ["order", "is_active", "show_on_home"]
    list_filter = ["group", "show_on_home", "is_active"]
    search_fields = ["name"]
    list_filter_submit = True

    @display(description="Texnologiya", header=True)
    def tech(self, obj):
        return [obj.name, obj.get_group_display(), obj.name[:2].upper(), thumb(obj.icon.url if obj.icon else None, 32)]


# --------------------------------------------------------------------------- Xizmatlar
@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ["title", "icon", "price_from", "order", "is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["title", "short"]


@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = ["position", "company", "period", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ["who", "rating", "order", "is_active"]
    list_editable = ["order", "is_active"]

    @display(description="Muallif", header=True)
    def who(self, obj):
        initials = "".join(p[0] for p in obj.author.split()[:2]).upper()
        return [obj.author, obj.position, initials, thumb(obj.avatar.url if obj.avatar else None, 32, True)]


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["brand", "url", "order", "is_active"]
    list_editable = ["order", "is_active"]

    @display(description="Mijoz", header=True)
    def brand(self, obj):
        return [obj.name, "", obj.name[:2].upper(), thumb(obj.logo.url if obj.logo else None, 32)]


# --------------------------------------------------------------------------- Brief / So'rovlar
@admin.register(ContactRequest)
class ContactRequestAdmin(ModelAdmin):
    list_display = ["who", "contact", "budget_label", "status_label", "created_at"]
    list_filter = [("status", ChoicesDropdownFilter), ("budget", ChoicesDropdownFilter), ("created_at", RangeDateFilter)]
    list_filter_submit = True
    search_fields = ["name", "phone", "email", "company", "message"]
    readonly_fields = ["name", "phone", "email", "company", "services", "budget", "message", "ip", "created_at"]
    fieldsets = (
        ("Mijoz", {"fields": ("name", "phone", "email", "company", "ip", "created_at")}),
        ("So'rov", {"fields": ("services", "budget", "message")}),
        ("Ish jarayoni", {"fields": ("status", "note")}),
    )
    actions = ["mark_in_progress", "mark_done", "mark_spam"]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    @display(description="Mijoz", header=True)
    def who(self, obj):
        initials = "".join(p[0] for p in obj.name.split()[:2]).upper()
        return [obj.name, obj.company or "", initials]

    @display(description="Aloqa")
    def contact(self, obj):
        tel = "".join(c for c in obj.phone if c.isdigit() or c == "+")
        return format_html('<a href="tel:{}">{}</a><br><span style="opacity:.6">{}</span>', tel, obj.phone, obj.email or "")

    @display(description="Byudjet", label=True)
    def budget_label(self, obj):
        return obj.get_budget_display()

    @display(
        description="Holat",
        label={
            "Yangi": "info",
            "Ko'rib chiqilmoqda": "warning",
            "Yakunlangan": "success",
            "Spam": "danger",
        },
    )
    def status_label(self, obj):
        return obj.get_status_display()

    @action(description="Ko'rib chiqilmoqda deb belgilash")
    def mark_in_progress(self, request, queryset):
        queryset.update(status=ContactRequest.Status.IN_PROGRESS)

    @action(description="Yakunlandi deb belgilash")
    def mark_done(self, request, queryset):
        queryset.update(status=ContactRequest.Status.DONE)

    @action(description="Spam deb belgilash")
    def mark_spam(self, request, queryset):
        queryset.update(status=ContactRequest.Status.SPAM)
