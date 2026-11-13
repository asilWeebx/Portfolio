from django.core.validators import FileExtensionValidator
from django.db import models


class TimeStamped(models.Model):
    created_at = models.DateTimeField("Yaratilgan", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan", auto_now=True)

    class Meta:
        abstract = True


class Ordered(models.Model):
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


# --------------------------------------------------------------------------- Sayt sozlamalari
class SiteSettings(models.Model):
    """Yagona yozuv (singleton) — saytning umumiy matnlari va kontaktlar."""

    # Hero
    full_name = models.CharField("To'liq ism", max_length=120, default="Asilbek Yuldoshev")
    role = models.CharField("Kasb / lavozim", max_length=120, default="Full-stack dasturchi")
    hero_title = models.CharField("Hero sarlavha", max_length=200, default="Raqamli yechimlar yarataman")
    hero_subtitle = models.CharField(
        "Hero kichik matn", max_length=300,
        default="Veb-saytlar, mobil ilovalar, Telegram botlar va biznes tizimlari — g'oyadan ishga tushirishgacha.",
    )
    available_for_work = models.BooleanField("Yangi loyihalarga ochiqman", default=True)

    # Men haqimda
    about_title = models.CharField("Men haqimda — sarlavha", max_length=200, default="Salom, men Asilbek")
    about_text = models.TextField("Men haqimda — matn", blank=True)
    avatar = models.ImageField("Rasm (avatar)", upload_to="site/", blank=True)
    about_photo = models.ImageField(
        "Ish jarayonidan rasm", upload_to="site/", blank=True,
        help_text="Bosh sahifadagi 'Men haqimda' blokida avatar yonida chiqadi",
    )
    cv_file = models.FileField(
        "Rezyume (PDF)", upload_to="site/", blank=True,
        validators=[FileExtensionValidator(["pdf"])],
    )

    # Raqamlar
    years_experience = models.PositiveIntegerField("Tajriba (yil)", default=3)
    happy_clients = models.PositiveIntegerField("Mijozlar soni", default=20)

    # Kontaktlar
    phone = models.CharField("Telefon", max_length=32, blank=True)
    email = models.EmailField("Email", blank=True)
    location = models.CharField("Manzil", max_length=120, default="Toshkent, O'zbekiston")
    telegram = models.URLField("Telegram", blank=True)
    github = models.URLField("GitHub", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    youtube = models.URLField("YouTube", blank=True)

    # SEO
    meta_description = models.CharField("SEO tavsif", max_length=300, blank=True)
    og_image = models.ImageField("Ijtimoiy tarmoq rasmi (1200x630)", upload_to="site/", blank=True)

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# --------------------------------------------------------------------------- Texnologiyalar
class Technology(Ordered):
    class Group(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        MOBILE = "mobile", "Mobil"
        DEVOPS = "devops", "DevOps / Server"
        DATABASE = "database", "Ma'lumotlar bazasi"
        TOOLS = "tools", "Vositalar"

    name = models.CharField("Nomi", max_length=60, unique=True)
    group = models.CharField("Guruh", max_length=20, choices=Group.choices, default=Group.BACKEND)
    icon = models.FileField(
        "Ikonka (SVG/PNG)", upload_to="tech/", blank=True,
        validators=[FileExtensionValidator(["svg", "png", "webp", "jpg", "jpeg"])],
    )
    color = models.CharField("Rang (hex)", max_length=9, blank=True, help_text="Masalan: #3776AB")
    show_on_home = models.BooleanField("Bosh sahifada ko'rsatish", default=True)

    class Meta(Ordered.Meta):
        verbose_name = "Texnologiya"
        verbose_name_plural = "Texnologiyalar"

    def __str__(self):
        return self.name


# --------------------------------------------------------------------------- Xizmatlar
class Service(Ordered):
    ICONS = [
        ("globe", "Veb-sayt"),
        ("smartphone", "Mobil ilova"),
        ("bot", "Telegram bot"),
        ("server", "Backend / API"),
        ("layout-dashboard", "CRM / ERP"),
        ("shopping-cart", "Onlayn do'kon"),
        ("palette", "UI/UX dizayn"),
        ("cloud", "Server / DevOps"),
        ("sparkles", "AI integratsiya"),
        ("wrench", "Qo'llab-quvvatlash"),
    ]

    title = models.CharField("Nomi", max_length=120)
    short = models.CharField("Qisqa tavsif", max_length=260)
    icon = models.CharField("Ikonka", max_length=40, choices=ICONS, default="globe")
    features = models.TextField(
        "Nimalar kiradi", blank=True,
        help_text="Har bir qatorga bitta punkt yozing",
    )
    price_from = models.CharField("Narx (dan)", max_length=60, blank=True, help_text="Masalan: $300 dan")

    class Meta(Ordered.Meta):
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"

    def __str__(self):
        return self.title

    @property
    def feature_list(self) -> list[str]:
        return [x.strip(" -•\t") for x in self.features.splitlines() if x.strip()]


# --------------------------------------------------------------------------- Tajriba
class Experience(Ordered):
    company = models.CharField("Kompaniya / Loyiha", max_length=120)
    position = models.CharField("Lavozim", max_length=120)
    period = models.CharField("Davr", max_length=60, help_text="Masalan: 2024 — hozir")
    description = models.TextField("Tavsif", blank=True)
    url = models.URLField("Havola", blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "Tajriba"
        verbose_name_plural = "Tajriba"

    def __str__(self):
        return f"{self.position} — {self.company}"


# --------------------------------------------------------------------------- Mijozlar
class Client(Ordered):
    name = models.CharField("Nomi", max_length=120)
    logo = models.FileField(
        "Logo", upload_to="clients/",
        validators=[FileExtensionValidator(["svg", "png", "webp", "jpg", "jpeg"])],
    )
    url = models.URLField("Sayt", blank=True)

    class Meta(Ordered.Meta):
        verbose_name = "Mijoz / Hamkor"
        verbose_name_plural = "Mijozlar / Hamkorlar"

    def __str__(self):
        return self.name


class Testimonial(Ordered):
    author = models.CharField("Ism", max_length=120)
    position = models.CharField("Lavozim / Kompaniya", max_length=160, blank=True)
    avatar = models.ImageField("Rasm", upload_to="testimonials/", blank=True)
    text = models.TextField("Fikr")
    rating = models.PositiveSmallIntegerField("Baho (1-5)", default=5)

    class Meta(Ordered.Meta):
        verbose_name = "Mijoz fikri"
        verbose_name_plural = "Mijozlar fikri"

    def __str__(self):
        return self.author


# --------------------------------------------------------------------------- Brief / So'rovlar
class ContactRequest(TimeStamped):
    class Status(models.TextChoices):
        NEW = "new", "Yangi"
        IN_PROGRESS = "in_progress", "Ko'rib chiqilmoqda"
        DONE = "done", "Yakunlangan"
        SPAM = "spam", "Spam"

    class Budget(models.TextChoices):
        S = "lt500", "$500 gacha"
        M = "500_1500", "$500 — $1 500"
        L = "1500_5000", "$1 500 — $5 000"
        XL = "gt5000", "$5 000 dan yuqori"
        UNKNOWN = "unknown", "Hali bilmayman"

    name = models.CharField("Ism", max_length=120)
    phone = models.CharField("Telefon", max_length=40)
    email = models.EmailField("Email", blank=True)
    company = models.CharField("Kompaniya", max_length=160, blank=True)
    services = models.ManyToManyField(Service, verbose_name="Xizmatlar", blank=True)
    budget = models.CharField("Byudjet", max_length=20, choices=Budget.choices, default=Budget.UNKNOWN)
    message = models.TextField("Xabar", blank=True)
    status = models.CharField("Holat", max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)
    note = models.TextField("Ichki izoh", blank=True)
    ip = models.GenericIPAddressField("IP", null=True, blank=True)

    class Meta:
        verbose_name = "Brief / So'rov"
        verbose_name_plural = "Brief / So'rovlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone})"
