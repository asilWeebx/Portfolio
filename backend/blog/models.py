import html
import math
import re

from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field

from core.models import TimeStamped
from portfolio.models import unique_slug


class Category(models.Model):
    """Blog mavzusi (rubrika)."""

    name = models.CharField("Nomi", max_length=80)
    slug = models.SlugField("Slug", max_length=100, unique=True, blank=True)
    description = models.CharField("Tavsif", max_length=260, blank=True)
    emoji = models.CharField("Ikonka (emoji)", max_length=8, blank=True)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Mavzu (rubrika)"
        verbose_name_plural = "Mavzular (rubrikalar)"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField("Nomi", max_length=50, unique=True)
    slug = models.SlugField("Slug", max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        super().save(*args, **kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(status=Post.Status.PUBLISHED, published_at__lte=timezone.now())
        )


class Post(TimeStamped):
    class Status(models.TextChoices):
        DRAFT = "draft", "Qoralama"
        PUBLISHED = "published", "Chop etilgan"

    title = models.CharField("Sarlavha", max_length=200)
    slug = models.SlugField("Slug (URL)", max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category, verbose_name="Mavzu", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="posts",
    )
    tags = models.ManyToManyField(Tag, verbose_name="Teglar", blank=True, related_name="posts")
    excerpt = models.CharField("Qisqa mazmun", max_length=320, blank=True, help_text="Ro'yxat va SEO uchun")
    cover = models.ImageField("Muqova rasmi", upload_to="blog/covers/", blank=True, help_text="Tavsiya: 1600x900")
    content = CKEditor5Field("Matn", config_name="default")

    status = models.CharField("Holat", max_length=12, choices=Status.choices, default=Status.DRAFT, db_index=True)
    published_at = models.DateTimeField("Chop etish sanasi", default=timezone.now, db_index=True)
    is_featured = models.BooleanField("Tanlangan", default=False)
    reading_time = models.PositiveIntegerField("O'qish vaqti (daq)", default=1, editable=False)
    views = models.PositiveIntegerField("Ko'rishlar", default=0, editable=False)

    seo_title = models.CharField("SEO sarlavha", max_length=160, blank=True)
    seo_description = models.CharField("SEO tavsif", max_length=300, blank=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        text = html.unescape(strip_tags(self.content or ""))
        words = len(re.findall(r"\w+", text))
        self.reading_time = max(1, math.ceil(words / 200))
        if not self.excerpt and text:
            clean = re.sub(r"\s+", " ", text).strip()
            self.excerpt = (clean[:297] + "...") if len(clean) > 300 else clean
        super().save(*args, **kwargs)
