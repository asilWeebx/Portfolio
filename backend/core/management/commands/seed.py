"""
Boshlang'ich ma'lumotlar: xizmatlar, texnologiyalar,
blog mavzulari, teglar, 3 ta namunaviy maqola va maqola g'oyalari (qoralama sifatida).

    python manage.py seed           # bo'sh bazaga yozadi (bor yozuvlarga tegmaydi)
    python manage.py seed --covers  # loyihalarga muqova rasmlarini qaytadan chizadi
"""
import io
import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from blog.models import Category, Post, Tag
from core.models import Experience, Service, SiteSettings, Technology


from ._seed_posts import DRAFT_IDEAS, POSTS

TECH = [
    # name, group, color
    ("Python", "backend", "#3776AB"),
    ("Django", "backend", "#0C4B33"),
    ("DRF", "backend", "#A30000"),
    ("FastAPI", "backend", "#009688"),
    ("Celery", "backend", "#37814A"),
    ("aiogram", "backend", "#26A5E4"),
    ("React", "frontend", "#61DAFB"),
    ("Next.js", "frontend", "#FFFFFF"),
    ("TypeScript", "frontend", "#3178C6"),
    ("Flutter", "mobile", "#02569B"),
    ("Dart", "mobile", "#0175C2"),
    ("PostgreSQL", "database", "#4169E1"),
    ("Redis", "database", "#DC382D"),
    ("Docker", "devops", "#2496ED"),
    ("Nginx", "devops", "#009639"),
    ("Linux", "devops", "#FCC624"),
    ("Git", "tools", "#F05032"),
    ("Figma", "tools", "#F24E1E"),
]

SERVICES = [
    ("Veb-saytlar", "globe", "Korporativ saytlar, landing sahifalar va portfoliolar — tez, SEO'ga tayyor, qulay admin panel bilan.",
     "Dizayn va maket\nAdmin panel (Django)\nSEO va tezlik optimizatsiyasi\nDomen, hosting, SSL", "$300 dan"),
    ("Mobil ilovalar", "smartphone", "Flutter'da iOS va Android uchun bitta kod bazasidan ishlaydigan ilovalar.",
     "iOS + Android\nPush-bildirishnomalar\nTo'lov tizimlari (Click, Payme)\nApp Store / Google Play'ga joylash", "$1 000 dan"),
    ("Telegram bot va Mini App", "bot", "Savdo, buyurtma, CRM va avtomatlashtirish uchun botlar hamda Telegram ichidagi do'konlar.",
     "Buyurtma va katalog\nTo'lov integratsiyasi\nAdmin panel va statistika\nMini App (veb-ilova)", "$200 dan"),
    ("CRM / ERP / POS", "layout-dashboard", "Savdo, ombor, kassa va moliyani bitta tizimda boshqarish — biznesingizga moslab.",
     "Kassa va sotuv\nOmbor, kirim, transfer\nNasiya va mijozlar bazasi\nHisobotlar va rollar", "Kelishiladi"),
    ("Backend va API", "server", "Django/DRF'da ishonchli, hujjatlashtirilgan API — mobil ilova va frontend uchun.",
     "REST API va hujjat\nAutentifikatsiya, rollar\nIntegratsiyalar (1C, Uzum, SMS)\nYuqori yuklamaga tayyorlash", "$400 dan"),
    ("Server va DevOps", "cloud", "Loyihani serverga chiqarish, avtomatik deploy, monitoring va zaxira nusxa.",
     "Ubuntu + Nginx + SSL\nDocker, CI/CD\nBackup va monitoring\nTezlik va xavfsizlik auditi", "$100 dan"),
]

PROJECT_CATS = ["Veb-sayt", "Mobil ilova", "Telegram bot", "CRM / ERP", "Onlayn do'kon"]

PROJECTS = [
    {
        "title": "Dukonline", "cat": "CRM / ERP", "year": 2026, "featured": True, "color": "#0F766E",
        "short": "Do'konlar uchun savdo boshqaruv tizimi: kassa, katalog, ombor, nasiya, hisobotlar va onlayn do'kon.",
        "role": "Full-stack", "url": "https://dukonline.uz",
        "tech": ["Django", "DRF", "Next.js", "TypeScript", "PostgreSQL", "Flutter"],
    },
    {
        "title": "Dukonline Optom", "cat": "Onlayn do'kon", "year": 2026, "featured": True, "color": "#7C3AED",
        "short": "Ulgurji savdo uchun e'lonlar marketpleysi: kategoriya, qidiruv, bonuslar va TOP-auksion.",
        "role": "Full-stack", "url": "",
        "tech": ["Django", "DRF", "React", "PostgreSQL"],
    },
    {
        "title": "CaseGo", "cat": "Telegram bot", "year": 2026, "featured": True, "color": "#2563EB",
        "short": "Telegram Mini App ichidagi onlayn do'kon: katalog, savat, buyurtma va admin panel.",
        "role": "Full-stack", "url": "https://app.casego.uz",
        "tech": ["Django", "React", "aiogram", "PostgreSQL", "Nginx"],
    },
    {
        "title": "Yoshlar ID", "cat": "Mobil ilova", "year": 2026, "featured": True, "color": "#0EA5E9",
        "short": "Yoshlar uchun milliy platformaning mobil ilovasi — Flutter'da iOS va Android.",
        "role": "Mobil dasturchi", "url": "",
        "tech": ["Flutter", "Dart", "Django"],
    },
    {
        "title": "SkillOra", "cat": "Veb-sayt", "year": 2025, "featured": True, "color": "#003366",
        "short": "IELTS imtihonining kompyuterdagi (CBT) muhitini aynan takrorlaydigan tayyorgarlik platformasi.",
        "role": "Full-stack", "url": "",
        "tech": ["Next.js", "TypeScript", "Django", "DRF"],
    },
    {
        "title": "Level-Up Homework", "cat": "Veb-sayt", "year": 2025, "featured": False, "color": "#16A34A",
        "short": "O'quv markazi uchun uy vazifalarini topshirish va tekshirish platformasi.",
        "role": "Backend", "url": "",
        "tech": ["Django", "Python"],
    },
    {
        "title": "Moliya bot", "cat": "Telegram bot", "year": 2026, "featured": False, "color": "#DB2777",
        "short": "Shaxsiy kirim-chiqimlarni Telegram orqali yuritish va hisobot olish uchun bot.",
        "role": "Backend", "url": "",
        "tech": ["Python", "aiogram", "PostgreSQL"],
    },
]

BLOG_CATS = [
    ("Backend va Django", "🐍", "Django, DRF, API dizayn, ma'lumotlar bazasi"),
    ("Frontend", "⚛️", "React, Next.js, TypeScript, UI"),
    ("Mobil (Flutter)", "📱", "Flutter va Dart'da iOS/Android ilovalar"),
    ("Telegram botlar", "🤖", "Botlar, Mini App, avtomatlashtirish"),
    ("DevOps va server", "🚀", "Linux, Nginx, Docker, deploy"),
    ("AI va avtomatlashtirish", "🧠", "LLM API'lar, botlarga AI ulash, ish jarayonini avtomatlashtirish"),
    ("Freelance va biznes", "💼", "Mijoz bilan ishlash, narxlash, loyiha boshqaruvi"),
    ("Karyera va o'qish", "📚", "Dasturlashni o'rganish, resurslar, talabalik"),
    ("Case study", "🔍", "Loyihalarim ichidan: qanday qurildi va nimani o'rgandim"),
]

TAGS = [
    "python", "django", "drf", "postgresql", "react", "nextjs", "typescript", "flutter",
    "telegram", "docker", "nginx", "linux", "seo", "freelance", "ai", "pos", "api", "startap",
]


def _font(size: int):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def make_cover(title: str, subtitle: str, color: str, kind: str, w=1600, h=1000) -> bytes:
    """Loyiha uchun vaqtinchalik muqova: qorong'i fon, rangli nur, qurilma maketi va sarlavha."""
    r, g, b = _hex(color)
    img = Image.new("RGB", (w, h), (20, 20, 21))
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((w * 0.45, -h * 0.35, w * 1.35, h * 0.85), fill=(r, g, b))
    gd.ellipse((-w * 0.3, h * 0.6, w * 0.4, h * 1.4), fill=(0, 167, 149))
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)

    rnd = random.Random(title)
    if kind in ("Mobil ilova", "Telegram bot"):
        # telefon maketi
        pw, ph = 330, 660
        x0, y0 = w - pw - 170, (h - ph) // 2 + 40
        d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=48, fill=(14, 14, 15), outline=(60, 60, 64), width=6)
        d.rounded_rectangle((x0 + 120, y0 + 18, x0 + pw - 120, y0 + 34), radius=8, fill=(40, 40, 44))
        y = y0 + 70
        d.rounded_rectangle((x0 + 28, y, x0 + pw - 28, y + 150), radius=22, fill=(r, g, b))
        y += 175
        for _ in range(5):
            d.rounded_rectangle((x0 + 28, y, x0 + 92, y + 64), radius=14, fill=(45, 45, 48))
            d.rounded_rectangle((x0 + 108, y + 10, x0 + pw - 40 - rnd.randint(0, 80), y + 26), radius=6, fill=(70, 70, 75))
            d.rounded_rectangle((x0 + 108, y + 38, x0 + pw - 100 - rnd.randint(0, 50), y + 52), radius=6, fill=(48, 48, 52))
            y += 80
    else:
        # brauzer maketi
        bw, bh = 820, 560
        x0, y0 = w - bw - 110, (h - bh) // 2 + 60
        d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=22, fill=(14, 14, 15), outline=(60, 60, 64), width=4)
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
            d.ellipse((x0 + 24 + i * 26, y0 + 20, x0 + 40 + i * 26, y0 + 36), fill=c)
        d.rounded_rectangle((x0 + 120, y0 + 16, x0 + bw - 120, y0 + 40), radius=10, fill=(32, 32, 35))
        # sidebar + kartochkalar
        d.rounded_rectangle((x0 + 20, y0 + 64, x0 + 180, y0 + bh - 20), radius=12, fill=(30, 30, 33))
        for i in range(6):
            d.rounded_rectangle((x0 + 36, y0 + 84 + i * 42, x0 + 160 - rnd.randint(0, 40), y0 + 100 + i * 42), radius=6,
                                fill=(r, g, b) if i == 0 else (55, 55, 60))
        cx = x0 + 200
        for i in range(3):
            d.rounded_rectangle((cx + i * 200, y0 + 64, cx + i * 200 + 184, y0 + 160), radius=12, fill=(30, 30, 33))
            d.rounded_rectangle((cx + i * 200 + 18, y0 + 84, cx + i * 200 + 90, y0 + 98), radius=5, fill=(70, 70, 75))
            d.rounded_rectangle((cx + i * 200 + 18, y0 + 112, cx + i * 200 + 130, y0 + 138), radius=6,
                                fill=(r, g, b) if i == 1 else (90, 90, 96))
        # grafik
        d.rounded_rectangle((cx, y0 + 176, x0 + bw - 20, y0 + bh - 20), radius=12, fill=(30, 30, 33))
        bars = 12
        bx = cx + 30
        for i in range(bars):
            bh_ = rnd.randint(60, 270)
            d.rounded_rectangle((bx + i * 46, y0 + bh - 46 - bh_, bx + i * 46 + 26, y0 + bh - 46), radius=6,
                                fill=(r, g, b) if i % 3 == 0 else (0, 167, 149))

    # sarlavha
    d.text((110, 140), kind.upper(), font=_font(30), fill=(0, 167, 149))
    d.text((106, 186), title, font=_font(96), fill=(255, 255, 255))
    words, line, lines = subtitle.split(), "", []
    for wd in words:
        if len(line + " " + wd) > 30:
            lines.append(line)
            line = wd
        else:
            line = (line + " " + wd).strip()
    lines.append(line)
    for i, ln in enumerate(lines[:4]):
        d.text((110, 330 + i * 46), ln, font=_font(32), fill=(170, 170, 175))

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=86, optimize=True)
    return buf.getvalue()


class Command(BaseCommand):
    help = "Boshlang'ich (namunaviy) ma'lumotlarni yaratadi"

    def add_arguments(self, parser):
        parser.add_argument("--covers", action="store_true", help="Loyiha muqovalarini qayta chizish")

    def handle(self, *args, covers=False, **opts):
        s = SiteSettings.load()
        if not s.about_text:
            s.about_text = (
                "Men Toshkentda yashovchi full-stack dasturchiman. Django va DRF'da backend, "
                "React va Next.js'da frontend, Flutter'da mobil ilovalar yarataman.\n\n"
                "Asosiy yo'nalishlarim — savdo va ombor tizimlari (POS/ERP), onlayn do'konlar, "
                "Telegram botlar va Mini App'lar. G'oyani tahlil qilishdan tortib serverga chiqarish va "
                "qo'llab-quvvatlashgacha bo'lgan butun jarayonni o'zim olib boraman.\n\n"
                "Blogimda o'zim duch kelgan muammolar va ularning yechimlari haqida yozaman — "
                "boshqalarga ham foydasi tegsin deb."
            )
            s.meta_description = (
                "Asilbek Yuldoshev — full-stack dasturchi. Veb-saytlar, mobil ilovalar, Telegram botlar, "
                "CRM/ERP va POS tizimlar. Portfolio va dasturlash haqida blog."
            )
            s.save()

        for i, (name, group, color) in enumerate(TECH):
            Technology.objects.get_or_create(name=name, defaults={"group": group, "color": color, "order": i})

        if not Service.objects.exists():
            for i, (title, icon, short, feats, price) in enumerate(SERVICES):
                Service.objects.create(title=title, icon=icon, short=short, features=feats, price_from=price, order=i)

        if not Experience.objects.exists():
            Experience.objects.create(
                company="Freelance", position="Full-stack dasturchi", period="2023 — hozir", order=0,
                description="Bizneslar uchun POS/ERP tizimlar, onlayn do'konlar, mobil ilovalar va Telegram botlar.",
            )
            Experience.objects.create(
                company="Inha University in Tashkent", position="Talaba", period="hozir", order=1,
                description="Dasturiy injiniring yo'nalishi.",
            )

        # Loyihalar: python manage.py import_projects (assets/project-shots'dan)
        bcats = {}
        for i, (name, emoji, desc) in enumerate(BLOG_CATS):
            bcats[name], _ = Category.objects.get_or_create(
                name=name, defaults={"emoji": emoji, "description": desc, "order": i},
            )
        tags = {}
        for t in TAGS:
            tags[t], _ = Tag.objects.get_or_create(name=t)

        now = timezone.now()
        for i, post in enumerate(POSTS):
            if Post.objects.filter(title=post["title"]).exists():
                continue
            obj = Post.objects.create(
                title=post["title"], category=bcats[post["category"]], excerpt=post["excerpt"],
                content=post["content"], status=Post.Status.PUBLISHED, is_featured=(i == 0),
                published_at=now - timezone.timedelta(days=3 + i * 6),
            )
            obj.tags.set([tags[t] for t in post["tags"] if t in tags])

        for idea in DRAFT_IDEAS:
            if Post.objects.filter(title=idea["title"]).exists():
                continue
            outline = "".join(f"<h2>{h}</h2><p>…</p>" for h in idea["outline"])
            obj = Post.objects.create(
                title=idea["title"], category=bcats[idea["category"]], excerpt=idea["excerpt"],
                content=f"<p><i>Reja (qoralama):</i></p>{outline}", status=Post.Status.DRAFT,
            )
            obj.tags.set([tags[t] for t in idea.get("tags", []) if t in tags])

        self.stdout.write(self.style.SUCCESS(
            f"Tayyor: {Post.objects.filter(status='published').count()} maqola, "
            f"{Post.objects.filter(status='draft').count()} qoralama g'oya, {Category.objects.count()} mavzu."
        ))
