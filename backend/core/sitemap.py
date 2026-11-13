"""Frontend sahifalari uchun sitemap.xml va robots.txt (Google indekslashi uchun)."""
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from blog.models import Category, Post
from portfolio.models import Project


@cache_page(60 * 30)
def sitemap_xml(request):
    base = settings.FRONTEND_URL
    urls: list[tuple[str, str | None, str]] = [
        (f"{base}/", None, "1.0"),
        (f"{base}/portfolio", None, "0.9"),
        (f"{base}/blog", None, "0.9"),
        (f"{base}/about", None, "0.7"),
        (f"{base}/brief", None, "0.6"),
    ]
    for p in Project.objects.filter(is_published=True).only("slug", "updated_at"):
        urls.append((f"{base}/portfolio/{p.slug}", p.updated_at.date().isoformat(), "0.8"))
    for p in Post.published.only("slug", "updated_at"):
        urls.append((f"{base}/blog/{p.slug}", p.updated_at.date().isoformat(), "0.8"))
    for c in Category.objects.only("slug"):
        urls.append((f"{base}/blog?category={c.slug}", None, "0.5"))

    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, prio in urls:
        body.append("<url>")
        body.append(f"<loc>{escape(loc)}</loc>")
        if lastmod:
            body.append(f"<lastmod>{lastmod}</lastmod>")
        body.append(f"<priority>{prio}</priority>")
        body.append("</url>")
    body.append("</urlset>")
    return HttpResponse("\n".join(body), content_type="application/xml")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        f"Sitemap: {settings.FRONTEND_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
