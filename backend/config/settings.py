"""
asilbek-yuldashev.uz — Django sozlamalari.
Barcha maxfiy qiymatlar .env faylidan olinadi (namuna: .env.example).
"""
import os
from pathlib import Path

import dj_database_url
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_list(name: str, default: str = "") -> list[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "http://localhost:5180")

# Frontend manzili (admin'dagi "Saytda ko'rish" va sitemap uchun)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5180").rstrip("/")

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "django_filters",
    "corsheaders",
    "django_ckeditor_5",
    # local
    "core",
    "portfolio",
    "blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# DATABASE_URL bo'lmasa — SQLite (lokal ishlab chiqish uchun)
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

# ---------------------------------------------------------------- DRF
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"]
    + (["rest_framework.renderers.BrowsableAPIRenderer"] if DEBUG else []),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 9,
    "DEFAULT_THROTTLE_RATES": {"contact": "5/hour"},
}

# ---------------------------------------------------------------- CORS
CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS", "http://localhost:5180")

# ---------------------------------------------------------------- Telegram
# Brief/kontakt formasi yuborilganda Telegram'ga xabar keladi (ixtiyoriy)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ---------------------------------------------------------------- Production xavfsizlik
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "SAMEORIGIN"

# ---------------------------------------------------------------- CKEditor 5
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_MAX_FILE_SIZE = 10  # MB
CKEDITOR_5_CUSTOM_CSS = "admin/ckeditor-dark.css"
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading", "|",
                "bold", "italic", "underline", "strikethrough", "code", "link", "highlight", "|",
                "bulletedList", "numberedList", "blockQuote", "|",
                "imageUpload", "mediaEmbed", "insertTable", "codeBlock", "horizontalLine", "|",
                "removeFormat", "sourceEditing", "undo", "redo",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraf", "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Sarlavha 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Sarlavha 3", "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Sarlavha 4", "class": "ck-heading_heading4"},
            ]
        },
        "image": {
            "toolbar": [
                "imageTextAlternative", "|",
                "imageStyle:alignLeft", "imageStyle:alignCenter", "imageStyle:alignRight", "|",
                "toggleImageCaption",
            ],
            "styles": ["full", "alignLeft", "alignCenter", "alignRight"],
        },
        "table": {"contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"]},
        "codeBlock": {
            "languages": [
                {"language": "plaintext", "label": "Oddiy matn"},
                {"language": "python", "label": "Python"},
                {"language": "javascript", "label": "JavaScript"},
                {"language": "typescript", "label": "TypeScript"},
                {"language": "dart", "label": "Dart"},
                {"language": "bash", "label": "Bash"},
                {"language": "sql", "label": "SQL"},
                {"language": "json", "label": "JSON"},
                {"language": "xml", "label": "HTML/XML"},
                {"language": "css", "label": "CSS"},
                {"language": "yaml", "label": "YAML"},
                {"language": "ini", "label": "INI / systemd"},
                {"language": "dockerfile", "label": "Dockerfile"},
                {"language": "nginx", "label": "Nginx"},
            ]
        },
        "mediaEmbed": {"previewsInData": True},
        "language": "en",
    },
}

# ---------------------------------------------------------------- Unfold admin
UNFOLD = {
    "SITE_TITLE": "Asilbek Yuldoshev — Admin",
    "SITE_HEADER": "Asilbek Yuldoshev",
    "SITE_SUBHEADER": "Portfolio & Blog boshqaruvi",
    "SITE_URL": FRONTEND_URL,
    "SITE_SYMBOL": "rocket_launch",
    "SITE_ICON": lambda request: static("brand/favicon.svg"),
    "SITE_FAVICONS": [
        {"rel": "icon", "sizes": "any", "type": "image/svg+xml", "href": lambda request: static("brand/favicon.svg")},
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "DASHBOARD_CALLBACK": "core.dashboard.dashboard_callback",
    "STYLES": [lambda request: static("admin/unfold-extra.css")],
    "BORDER_RADIUS": "10px",
    "COLORS": {
        # zinc — saytning qorong'i foniga mos
        "base": {
            "50": "oklch(98.5% 0 0)",
            "100": "oklch(96.7% .001 286.375)",
            "200": "oklch(92% .004 286.32)",
            "300": "oklch(87.1% .006 286.286)",
            "400": "oklch(70.5% .015 286.067)",
            "500": "oklch(55.2% .016 285.938)",
            "600": "oklch(44.2% .017 285.786)",
            "700": "oklch(37% .013 285.805)",
            "800": "oklch(27.4% .006 286.033)",
            "900": "oklch(21% .006 285.885)",
            "950": "oklch(14.1% .005 285.823)",
        },
        # indigo — brend rangi #5B4CF0
        "primary": {
            "50": "oklch(96.2% .018 272.314)",
            "100": "oklch(93% .034 272.788)",
            "200": "oklch(87% .065 274.039)",
            "300": "oklch(78.5% .115 274.713)",
            "400": "oklch(67.3% .182 276.935)",
            "500": "oklch(58.5% .233 277.117)",
            "600": "oklch(53% .24 277)",
            "700": "oklch(45.7% .24 277.023)",
            "800": "oklch(39.8% .195 277.366)",
            "900": "oklch(35.9% .144 278.697)",
            "950": "oklch(25.7% .09 281.288)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Asosiy"),
                "items": [
                    {"title": _("Boshqaruv paneli"), "icon": "dashboard", "link": reverse_lazy("admin:index")},
                    {"title": _("Sayt sozlamalari"), "icon": "tune", "link": reverse_lazy("admin:core_sitesettings_changelist")},
                    {
                        "title": _("Brief / So'rovlar"),
                        "icon": "mail",
                        "link": reverse_lazy("admin:core_contactrequest_changelist"),
                        "badge": "core.dashboard.unread_requests_badge",
                    },
                ],
            },
            {
                "title": _("Portfolio"),
                "items": [
                    {"title": _("Loyihalar"), "icon": "work", "link": reverse_lazy("admin:portfolio_project_changelist")},
                    {"title": _("Loyiha turlari"), "icon": "category", "link": reverse_lazy("admin:portfolio_projectcategory_changelist")},
                    {"title": _("Texnologiyalar"), "icon": "memory", "link": reverse_lazy("admin:core_technology_changelist")},
                ],
            },
            {
                "title": _("Blog"),
                "items": [
                    {"title": _("Maqolalar"), "icon": "article", "link": reverse_lazy("admin:blog_post_changelist")},
                    {"title": _("Mavzular (rubrika)"), "icon": "folder", "link": reverse_lazy("admin:blog_category_changelist")},
                    {"title": _("Teglar"), "icon": "sell", "link": reverse_lazy("admin:blog_tag_changelist")},
                ],
            },
            {
                "title": _("Sahifa bloklari"),
                "items": [
                    {"title": _("Xizmatlar"), "icon": "design_services", "link": reverse_lazy("admin:core_service_changelist")},
                    {"title": _("Tajriba"), "icon": "timeline", "link": reverse_lazy("admin:core_experience_changelist")},
                    {"title": _("Mijozlar fikri"), "icon": "reviews", "link": reverse_lazy("admin:core_testimonial_changelist")},
                    {"title": _("Mijozlar / Hamkorlar"), "icon": "handshake", "link": reverse_lazy("admin:core_client_changelist")},
                ],
            },
            {
                "title": _("Tizim"),
                "items": [
                    {"title": _("Foydalanuvchilar"), "icon": "person", "link": reverse_lazy("admin:auth_user_changelist")},
                ],
            },
        ],
    },
}
