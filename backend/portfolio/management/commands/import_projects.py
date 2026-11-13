"""
Haqiqiy loyihalarni assets/project-shots papkasidan import qiladi:
mockup muqova chizadi, rasmlarni WebP'ga siqadi, store havolalarini yozadi.

    python manage.py import_projects                       # standart papka: ../assets/project-shots
    python manage.py import_projects --dir /yo'l/papka
    python manage.py import_projects --replace             # mavjud loyihalarni o'chirib, qaytadan yaratadi
"""
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from core.models import Technology
from portfolio.mockups import compose_cover, to_webp
from portfolio.models import Project, ProjectCategory, ProjectImage

AS = "https://apps.apple.com/uz/app"
GP = "https://play.google.com/store/apps/details?id="

PROJECTS = [
    {
        "slug": "dukonline", "title": "Dukonline", "cat": "CRM / ERP", "color": "#E4572E", "featured": True,
        "short": "Do'konlar va optom savdo uchun SaaS POS/ERP: kassa, ombor, nasiya daftari, filiallar, hisobotlar va onlayn do'kon.",
        "role": "Asoschi, full-stack", "client": "O'z mahsulotim",
        "live": "https://dukonline.uz", "ios": f"{AS}/dukonline/id6792541398", "android": f"{GP}com.dukonline.dukonline_app",
        "has_desktop": True,
        "tech": ["Django", "DRF", "Next.js", "React", "TypeScript", "Flutter", "PostgreSQL", "Redis"],
        "cover": {"desktop": "desktop.png", "posters": ["store-4.png"]},
        "gallery": ["desktop.png", "store-1.png", "store-2.png", "store-3.png", "store-4.png", "store-5.png", "docs.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Kichik va o'rta do'konlar savdo, ombor va qarzlarni hali ham daftarda yoki bir-biriga bog'lanmagan dasturlarda yuritadi. Maqsad — kassadan tortib onlayn do'kongacha hammasini bitta tizimga yig'ish.</p>
<h2>Yechim</h2>
<p>Dukonline — veb, mobil (iOS/Android) va desktop kassa ilovasidan iborat SaaS platforma. Bitta akkaunt bilan bir nechta filial, kassa va xodimlarni boshqarish mumkin.</p>
<ul>
<li>Kassa va tez sotuv, smena, chek</li>
<li>Katalog, variantli tovarlar, kirim, transfer, reviziya</li>
<li>Nasiya va qarz daftari, mijozlar bazasi</li>
<li>Hisobotlar, rollar va ruxsatlar</li>
<li>Onlayn do'kon (storefront API) va Uzum integratsiyasi</li>
</ul>
<h2>Texnik tomoni</h2>
<p>Backend — Django + DRF + Channels, veb panel — Next.js / React, mobil va desktop — bitta Flutter kod bazasi. Tizim ustida bir nechta mijoz do'konlari (Zootopiya, Lux Home, Kafel Baraka, Kiddos va boshqalar) ishlaydi.</p>
""",
    },
    {
        "slug": "dukonline-pos", "title": "Dukonline POS", "cat": "CRM / ERP", "color": "#1F2433", "featured": True,
        "short": "Kassa kompyuteri uchun desktop POS: tez sotuv, PIN bilan qulflash, smena, qarz daftari va hisobotlar — Windows va macOS.",
        "role": "Flutter dasturchi", "client": "Dukonline",
        "has_desktop": True,
        "tech": ["Flutter", "Dart", "Django", "DRF"],
        "cover": {"desktop": "pos-1.png"},
        "gallery": ["pos-1.png", "pos-2.png", "pos-3.png", "pos-4.png"],
        "logo": None, "logo_from": "dukonline/icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Kassir uchun tez, sichqonchasiz ham ishlaydigan va internet uzilganda to'xtab qolmaydigan kassa dasturi kerak edi.</p>
<h2>Yechim</h2>
<p>Dukonline mobil ilovasining Flutter kod bazasi Windows va macOS uchun desktop ilova sifatida yig'ildi. Natijada bitta kod — uchta platforma.</p>
<ul>
<li>Shtrix-kod skaneri bilan tez sotuv</li>
<li>PIN bilan qulflash va smena</li>
<li>Qarz daftari va hisobotlar</li>
</ul>
""",
    },
    {
        "slug": "casego", "title": "CaseGo", "cat": "Onlayn do'kon", "color": "#2457F5", "featured": True,
        "short": "Telefon aksessuarlari ulgurji do'koni: sayt, Telegram Mini App va admin panel; katalog iBox ERP'dan sinxronlanadi.",
        "role": "Full-stack", "client": "CaseGo",
        "live": "https://casego.uz", "android": f"{GP}com.casego.app", "telegram": "https://t.me/casegooptombot",
        "tech": ["Django", "DRF", "Celery", "Redis", "PostgreSQL", "Next.js", "Docker"],
        "cover": {"desktop": "desktop.png", "tablet": "store-1.png"},
        "gallery": ["desktop.png", "store-1.png", "store-2.png", "store-3.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Ulgurji mijozlar katalogni ko'rib, buyurtmani tez berishi va xodimlar uni darhol ko'rishi kerak edi.</p>
<h2>Yechim</h2>
<ul>
<li>Telegram Mini App va sayt — bitta backend ustida</li>
<li>Katalog va qoldiqlar iBox (SMPro) ERP'dan avtomatik olinadi</li>
<li>Buyurtmalar bazada saqlanadi, xodimlarga Telegram bot orqali xabar keladi</li>
<li>Planshet uchun Android ilova</li>
</ul>
""",
    },
    {
        "slug": "zootopiya", "title": "Zootopiya", "cat": "Onlayn do'kon", "color": "#1E5B3B", "featured": True,
        "short": "Uy hayvonlari uchun zoomagazin: sayt va mobil ilova, ozuqa kalkulyatori; narx va qoldiq Dukonline ERP'dan olinadi.",
        "role": "Full-stack", "client": "Zootopiya",
        "live": "https://zootopiya.uz", "ios": f"{AS}/zootopiya/id6801299765", "android": f"{GP}com.mirsolioptom.store_app",
        "tech": ["Flutter", "Dart", "Next.js", "Django"],
        "cover": {"desktop": "desktop.png", "phone": "store-1.png"},
        "gallery": ["desktop.png", "store-1.png", "store-2.png", "store-3.png", "store-4.png", "store-5.png", "store-6.png", "store-7.png", "store-8.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Zoomagazinga mijozlar uydan turib ozuqa va aksessuar buyurtma qila oladigan sayt va ilova kerak edi.</p>
<h2>Yechim</h2>
<ul>
<li>Sayt va iOS/Android ilova — katalog, savat, buyurtma</li>
<li>Hayvon vazni va faolligiga qarab ozuqa kalkulyatori</li>
<li>Narx va qoldiqlar Dukonline ERP'dan real vaqtda</li>
<li>Doimiy mijozlar uchun mijoz ID orqali kirish</li>
</ul>
""",
    },
    {
        "slug": "kafel-baraka", "title": "Kafel Baraka", "cat": "Onlayn do'kon", "color": "#2B2620", "featured": True,
        "short": "Kafel va keramogranit do'koni: m² bo'yicha narx, kafel kalkulyatori va optom yetkazib berish — sayt va mobil ilova.",
        "role": "Full-stack", "client": "Kafel Baraka",
        "live": "https://kafelbaraka.uz", "ios": f"{AS}/kafel-baraka/id6795895961", "android": f"{GP}com.kafelbaraka.store_app",
        "tech": ["Flutter", "Dart", "Next.js", "Django"],
        "cover": {"desktop": "desktop.png", "phone": "store-1.png"},
        "gallery": ["desktop.png", "store-1.png", "store-2.png", "store-3.png", "store-4.png", "store-5.png", "store-6.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Kafel sotishda mijoz uchun eng muhim savol — "xonamga necha quti kerak?". Shu savolga ilovaning o'zi javob berishi kerak edi.</p>
<h2>Yechim</h2>
<ul>
<li>Narxlar m² va quti bo'yicha, avtomatik hisob</li>
<li>Kafel kalkulyatori: xona o'lchami bo'yicha kerakli miqdor</li>
<li>Filtrlar: o'lcham, sirt, kolleksiya</li>
<li>Optom buyurtma va yetkazib berish</li>
</ul>
""",
    },
    {
        "slug": "lux-home", "title": "Lux Home", "cat": "Onlayn do'kon", "color": "#7A5B3A", "featured": True,
        "short": "Uy-ro'zg'or va oshxona buyumlari onlayn do'koni va mobil ilovasi; katalog Dukonline ERP bilan bog'langan.",
        "role": "Full-stack", "client": "Lux Home",
        "live": "https://lux-home.uz", "ios": f"{AS}/lux-home/id6795919899", "android": f"{GP}com.luxhome.store_app",
        "tech": ["Flutter", "Dart", "Next.js", "Django"],
        "cover": {"desktop": "desktop.png", "posters": ["store-1.png"]},
        "gallery": ["desktop.png", "store-1.png", "store-2.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Uy buyumlari do'koniga premium ko'rinishdagi sayt va mobil ilova kerak edi.</p>
<h2>Yechim</h2>
<ul>
<li>Sayt va iOS/Android ilova</li>
<li>Katalog, filtrlar, savat va buyurtma</li>
<li>Narx va qoldiqlar Dukonline ERP'dan</li>
</ul>
""",
    },
    {
        "slug": "kiddos-uzbekistan", "title": "Kiddos Uzbekistan", "cat": "Onlayn do'kon", "color": "#1667D9", "featured": True,
        "short": "Bolalar poyabzali ulgurji savdosi: katalog faqat hamkor do'konlarga mijoz ID orqali ochiladi.",
        "role": "Full-stack", "client": "Kiddos Uzbekistan",
        "live": "https://kiddosuzbekistan.uz", "ios": f"{AS}/kiddos-uzbekistan/id6826551194",
        "tech": ["Flutter", "Dart", "Next.js", "Django"],
        "cover": {"desktop": "desktop.png", "phone": "store-1.png"},
        "gallery": ["desktop.png", "store-1.png", "store-2.png", "store-3.png", "store-4.png", "store-5.png", "store-6.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Ulgurji narxlar faqat hamkor do'konlarga ko'rinishi, chakana xaridorlarga esa yopiq bo'lishi kerak edi.</p>
<h2>Yechim</h2>
<ul>
<li>B2B katalog: kirish mijoz ID orqali</li>
<li>Model, o'lcham va korobka bo'yicha buyurtma</li>
<li>Sayt va iOS ilova, narx va qoldiq Dukonline'dan</li>
</ul>
""",
    },
    {
        "slug": "fariza-optom", "title": "Fariza Optom", "cat": "Onlayn do'kon", "color": "#15703F", "featured": True,
        "short": "Parfyumeriya va maishiy kimyo optom do'koni: sayt, Telegram Mini App va do'kon bazasi bilan sinxronlaydigan Windows connector.",
        "role": "Full-stack", "client": "Fariza Optom",
        "live": "https://farizaoptom.uz", "has_desktop": True,
        "tech": ["Django", "DRF", "Celery", "Next.js", "Python"],
        "cover": {"desktop": "desktop.png"},
        "gallery": ["desktop.png"],
        "logo": "connector-icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Do'kon katalogi va qoldiqlari kompyuterdagi EasyTrade/REGOS dasturida. Saytni shu bilan bog'lash kerak edi — oq IP va port ochmasdan.</p>
<h2>Yechim</h2>
<ul>
<li>Sayt va Telegram Mini App, admin panel</li>
<li><b>FARIZA connector</b> — Windows dasturi: do'kon bazasini faqat o'qiydi, katalog va qoldiqni HTTPS orqali saytga yuboradi, buyurtmalarni qaytarib oladi</li>
<li>Oq IP ham, port ochish ham shart emas</li>
</ul>
""",
    },
    {
        "slug": "level-up", "title": "Level-Up", "cat": "Mobil ilova", "color": "#F6B800", "featured": True,
        "short": "Ingliz tili o'quv markazi talabalari uchun ilova: uy vazifalari, coin va mukofotlar, tadbirlar, support-teacher bron qilish.",
        "role": "Full-stack", "client": "Level Up o'quv markazi",
        "ios": f"{AS}/level-up-student-app/id6758109160", "android": f"{GP}com.levelupstudent.levelup_app",
        "tech": ["Django", "DRF", "Flutter", "Dart"],
        "cover": {"posters": ["store-2.png", "store-1.png", "store-4.png"]},
        "gallery": ["store-1.png", "store-2.png", "store-3.png", "store-4.png", "store-5.png", "store-6.png", "store-7.png", "store-8.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>O'quv markazi talabalarni uy vazifasini muntazam bajarishga undaydigan va o'qituvchilar ishini yengillashtiradigan tizim so'radi.</p>
<h2>Yechim</h2>
<ul>
<li>Talabalar uchun iOS/Android ilova: unit va uy vazifalari</li>
<li>Coin tizimi va mukofotlar do'koni</li>
<li>Tadbirlar va support-teacher'ga bron qilish</li>
<li>O'qituvchi, admin va support uchun veb panel</li>
</ul>
""",
    },
    {
        "slug": "dukonline-optom", "title": "Dukonline Optom", "cat": "Onlayn do'kon", "color": "#1E4FE0", "featured": True,
        "short": "OLX uslubidagi optom e'lonlar platformasi: ostatka tovarlar, moderatsiya, chat, TOP reyting auksioni, Payme/Click.",
        "role": "Full-stack", "client": "O'z mahsulotim",
        "tech": ["Django", "DRF", "Celery", "Redis", "PostgreSQL", "Next.js", "Flutter"],
        "cover": {"desktop": "og.png"},
        "gallery": ["og.png"],
        "logo": "icon.png",
        "content": """
<h2>Vazifa</h2>
<p>Ulgurji sotuvchilarda mavsumdan qolgan, ortiqcha yoki likvidatsiya qilinadigan tovarlar (ostatka) ko'p. Ularni boshqa optomchilarga tez sotish uchun ixtisoslashgan maydon yo'q edi.</p>
<h2>Yechim</h2>
<ul>
<li>E'lonlar: qoralama → moderatsiya → 30 kun faol</li>
<li>Sotuvchi va xaridor o'rtasida chat (real vaqt)</li>
<li>TOP reyting — haftalik auksion: "bu o'rinni X so'mga egallash"</li>
<li>Pullik xizmatlar, Payme va Click orqali to'lov</li>
<li>Veb-sayt va Flutter mobil ilova bitta API ustida</li>
</ul>
""",
    },
    {
        "slug": "uzbekistan-economic-assembly", "title": "Iqtisodiyot Assambleyasi", "cat": "Veb-sayt", "color": "#18235A", "featured": True,
        "short": "O'zbekiston iqtisodiyot assambleyasining rasmiy sayti: tuzilma, loyihalar, assotsiatsiyalar va yangiliklar.",
        "role": "Frontend", "client": "O'zbekiston iqtisodiyot assambleyasi",
        "live": "https://assembly.uz/ru",
        "tech": ["Next.js", "TypeScript"],
        "cover": {"desktop": "desktop-live.png"},
        "gallery": ["desktop-live.png"],
        "logo": None,
        "content": """
<h2>Yechim</h2>
<p>O'zbekiston iqtisodiyot assambleyasi uchun zamonaviy korporativ sayt: assambleya tuzilmasi, xizmatlar, loyihalar, assotsiatsiyalar va yangiliklar bo'limlari, ko'p tilli interfeys.</p>
""",
    },
    {
        "slug": "prorabbob", "title": "ProRabBOB", "cat": "Veb-sayt", "color": "#151515", "featured": True,
        "short": "Asfalt yotqizish va yo'l qurilishi kompaniyasi sayti: xizmatlar, bajarilgan ishlar va buyurtma formasi.",
        "role": "Full-stack", "client": "ProRabBOB",
        "live": "https://prorabbob.uz",
        "tech": ["JavaScript"],
        "cover": {"desktop": "desktop.png"},
        "gallery": ["desktop.png"],
        "logo": None,
        "content": """
<h2>Yechim</h2>
<p>Yo'l qurilishi kompaniyasi uchun brendga mos, qora-sariq uslubdagi sayt: raqamlarda tajriba, xizmatlar, portfolio va onlayn buyurtma formasi.</p>
""",
    },
    {
        "slug": "level-up-karshi", "title": "Level Up Qarshi", "cat": "Veb-sayt", "color": "#F2B600", "featured": False,
        "short": "Ingliz tili o'quv markazi sayti: kurslar, ustozlar, markaz haqida va kursga yozilish formasi.",
        "role": "Frontend", "client": "Level Up o'quv markazi",
        "live": "https://level-up-karshi.uz",
        "tech": ["JavaScript"],
        "cover": {"desktop": "desktop-live.png"},
        "gallery": ["desktop-live.png"],
        "logo": None, "logo_from": "levelup-homework/icon.png",
        "content": """
<h2>Yechim</h2>
<p>O'quv markazi uchun landing sayt: kurslar ro'yxati (0 dan IELTS gacha), ustozlar, manzil va kontaktlar, kursga yozilish formasi. Level-Up mobil ilovasi bilan bir brendda.</p>
""",
    },
    {
        "slug": "dubai-express-mobile", "title": "Dubai Express Mobile", "cat": "Onlayn do'kon", "color": "#B4161B", "featured": False,
        "short": "iPhone va smartfonlar (yangi va b/u) do'koni sayti; tovar va qoldiqlar Dukonline API orqali.",
        "role": "Frontend, integratsiya", "client": "Dubai Express Mobile",
        "live": "https://dubaiexpressmobile.uz",
        "tech": ["Next.js", "Django"],
        "cover": {"desktop": "desktop.png"},
        "gallery": ["desktop.png"],
        "logo": "logo.png",
        "content": """
<h2>Yechim</h2>
<p>Smartfonlar do'koni uchun zamonaviy katalog sayti. Tovarlar, narxlar va qoldiqlar do'konning Dukonline tizimidan avtomatik olinadi — sotuvchi saytni alohida yangilamaydi.</p>
""",
    },
    {
        "slug": "san-hydro-energy", "title": "SAN HYDRO ENERGY", "cat": "Veb-sayt", "color": "#A3162B", "featured": False,
        "short": "Tomchilatib sug'orish va mini GES kompaniyasi sayti — mahsulotlar do'koni Dukonline API orqali.",
        "role": "Frontend", "client": "SAN HYDRO ENERGY",
        "live": "https://www.san-hydro.uz",
        "tech": ["Next.js", "TypeScript"],
        "cover": {"desktop": "desktop.png"},
        "gallery": ["desktop.png"],
        "logo": None,
        "content": """
<h2>Yechim</h2>
<p>Kompaniya xizmatlari, loyihalari va mahsulotlar katalogi bilan korporativ sayt. Do'kon qismi Dukonline API orqali ishlaydi.</p>
""",
    },
]

FOLDERS = {
    "dukonline": "dukonline", "dukonline-pos": "dukonline-pos", "casego": "casego", "zootopiya": "zootopiya",
    "kafel-baraka": "kafelbaraka", "lux-home": "luxhome", "kiddos-uzbekistan": "kiddos", "fariza-optom": "fariza-optom",
    "level-up": "levelup-homework", "dubai-express-mobile": "dubai-express-mobile", "san-hydro-energy": "san-hydro-energy",
    "dukonline-optom": "dukonline-optom", "uzbekistan-economic-assembly": "economic-assembly", "prorabbob": "prorabbob",
    "level-up-karshi": "level-up-karshi",
}
CATS = ["Onlayn do'kon", "CRM / ERP", "Mobil ilova", "Veb-sayt", "Telegram bot"]
EXTRA_TECH = [("React", "frontend", "#61DAFB"), ("JavaScript", "frontend", "#F7DF1E")]


class Command(BaseCommand):
    help = "assets/project-shots'dan haqiqiy loyihalarni import qiladi"

    def add_arguments(self, parser):
        parser.add_argument("--dir", default=str(Path(settings.BASE_DIR).parent / "assets" / "project-shots"))
        parser.add_argument("--replace", action="store_true", help="Barcha mavjud loyihalarni o'chirib, qaytadan yaratish")
        parser.add_argument("--only", help="Faqat shu slug(lar), vergul bilan")

    def handle(self, *args, **o):
        root = Path(o["dir"])
        if not root.exists():
            self.stderr.write(f"Papka topilmadi: {root}")
            return
        only = set(o["only"].split(",")) if o.get("only") else None

        if o["replace"]:
            for p in Project.objects.all():
                for f in (p.cover, p.logo):
                    if f:
                        f.delete(save=False)
                for img in p.images.all():
                    img.image.delete(save=False)
                p.delete()

        for name, group, color in EXTRA_TECH:
            Technology.objects.get_or_create(name=name, defaults={"group": group, "color": color})
        cats = {}
        for i, n in enumerate(CATS):
            cats[n], _ = ProjectCategory.objects.get_or_create(name=n, defaults={"order": i})
        techs = {t.name: t for t in Technology.objects.all()}

        for order, spec in enumerate(PROJECTS):
            if only and spec["slug"] not in only:
                continue
            folder = root / FOLDERS[spec["slug"]]
            p = Project.objects.filter(slug=spec["slug"]).first() or Project(slug=spec["slug"])
            p.title = spec["title"]
            p.category = cats[spec["cat"]]
            p.short_description = spec["short"]
            p.content = spec["content"].strip()
            p.accent_color = spec["color"]
            p.role = spec.get("role", "")
            p.client = spec.get("client", "")
            p.live_url = spec.get("live", "")
            p.app_store_url = spec.get("ios", "")
            p.play_store_url = spec.get("android", "")
            p.telegram_url = spec.get("telegram", "")
            p.has_desktop = spec.get("has_desktop", False)
            p.is_featured = spec.get("featured", False)
            p.is_published = True
            p.order = order

            cv = {k: (str(folder / v) if isinstance(v, str) else [str(folder / x) for x in v]) for k, v in spec["cover"].items()}
            if p.cover:
                p.cover.delete(save=False)
            p.cover.save(f"{spec['slug']}.webp", ContentFile(compose_cover(**cv)), save=False)

            logo_path = folder / spec["logo"] if spec.get("logo") else (root / spec["logo_from"] if spec.get("logo_from") else None)
            if logo_path and logo_path.exists():
                if p.logo:
                    p.logo.delete(save=False)
                p.logo.save(f"{spec['slug']}.webp", ContentFile(to_webp(str(logo_path), 256)), save=False)
            p.save()
            p.technologies.set([techs[t] for t in spec["tech"] if t in techs])

            for img in p.images.all():
                img.image.delete(save=False)
                img.delete()
            for i, g in enumerate(spec["gallery"]):
                path = folder / g
                if not path.exists():
                    continue
                portrait = g.startswith("store")
                data = to_webp(str(path), 900 if portrait else 1800)
                pi = ProjectImage(project=p, order=i)
                pi.image.save(f"{spec['slug']}-{i + 1}.webp", ContentFile(data), save=True)
            self.stdout.write(f"✓ {p.title}: {p.images.count()} rasm")

        self.stdout.write(self.style.SUCCESS(f"Jami chop etilgan loyihalar: {Project.objects.filter(is_published=True).count()}"))
