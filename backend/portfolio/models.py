from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from core.models import Ordered, Technology, TimeStamped


def unique_slug(instance, value: str, field: str = "slug") -> str:
    base = slugify(value, allow_unicode=False)[:180] or "item"
    slug, n = base, 2
    model = type(instance)
    while model.objects.filter(**{field: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


class ProjectCategory(Ordered):
    name = models.CharField("Nomi", max_length=80)
    slug = models.SlugField("Slug", max_length=100, unique=True, blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "Loyiha turi"
        verbose_name_plural = "Loyiha turlari"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        super().save(*args, **kwargs)


class Project(TimeStamped):
    title = models.CharField("Nomi", max_length=160)
    slug = models.SlugField("Slug (URL)", max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory, verbose_name="Turi", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="projects",
    )
    short_description = models.CharField("Qisqa tavsif", max_length=300)
    content = CKEditor5Field("Batafsil (case study)", config_name="default", blank=True)
    cover = models.ImageField(
        "Muqova (mockup)", upload_to="projects/covers/",
        help_text="Shaffof fonli PNG/WebP mockup tavsiya etiladi (1600x1200) — kartochka rangi orqasida ko'rinadi",
    )
    logo = models.FileField(
        "Logo / ilova ikonkasi", upload_to="projects/logos/", blank=True,
        validators=[FileExtensionValidator(["svg", "png", "webp", "jpg", "jpeg"])],
    )
    accent_color = models.CharField(
        "Aksent rang", max_length=9, blank=True,
        help_text="Kartochka foni (brend rangi), masalan #1E3A8A",
    )

    client = models.CharField("Mijoz", max_length=160, blank=True)
    role = models.CharField("Mening rolim", max_length=160, blank=True, help_text="Masalan: Full-stack, Backend")
    year = models.PositiveIntegerField("Yil", null=True, blank=True)
    duration = models.CharField("Davomiyligi", max_length=60, blank=True, help_text="Masalan: 3 oy")
    technologies = models.ManyToManyField(Technology, verbose_name="Texnologiyalar", blank=True, related_name="projects")

    live_url = models.URLField("Sayt havolasi", blank=True)
    github_url = models.URLField("GitHub", blank=True)
    app_store_url = models.URLField("App Store", blank=True)
    play_store_url = models.URLField("Google Play", blank=True)
    telegram_url = models.URLField("Telegram bot", blank=True)
    desktop_url = models.URLField("Desktop versiya (yuklab olish)", blank=True)
    has_desktop = models.BooleanField("Desktop versiyasi bor", default=False, help_text="Havola bo'lmasa ham belgini ko'rsatish")

    is_featured = models.BooleanField("Tanlangan (bosh sahifada)", default=False)
    is_published = models.BooleanField("Chop etilgan", default=True)
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)

    seo_title = models.CharField("SEO sarlavha", max_length=160, blank=True)
    seo_description = models.CharField("SEO tavsif", max_length=300, blank=True)

    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ["order", "-year", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        super().save(*args, **kwargs)

    @property
    def platforms(self) -> list[str]:
        out = []
        if self.live_url:
            out.append("web")
        if self.play_store_url:
            out.append("android")
        if self.app_store_url:
            out.append("ios")
        if self.desktop_url or self.has_desktop:
            out.append("desktop")
        if self.telegram_url:
            out.append("telegram")
        return out


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Rasm", upload_to="projects/gallery/")
    caption = models.CharField("Izoh", max_length=200, blank=True)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Galereya"
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Rasm #{self.pk}"
