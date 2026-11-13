from datetime import timedelta

from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone

from blog.models import Post
from portfolio.models import Project

from .models import ContactRequest


def unread_requests_badge(request):
    n = ContactRequest.objects.filter(status=ContactRequest.Status.NEW).count()
    return n or None


def dashboard_callback(request, context):
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    posts = Post.objects.all()

    cards = [
        {
            "title": "Loyihalar",
            "value": Project.objects.filter(is_published=True).count(),
            "hint": f"{Project.objects.filter(is_featured=True).count()} tasi tanlangan",
            "icon": "work",
            "href": reverse("admin:portfolio_project_changelist"),
        },
        {
            "title": "Maqolalar",
            "value": posts.filter(status=Post.Status.PUBLISHED).count(),
            "hint": f"{posts.filter(status=Post.Status.DRAFT).count()} ta qoralama",
            "icon": "article",
            "href": reverse("admin:blog_post_changelist"),
        },
        {
            "title": "Blog ko'rishlari",
            "value": posts.aggregate(s=Sum("views"))["s"] or 0,
            "hint": "jami",
            "icon": "visibility",
            "href": reverse("admin:blog_post_changelist"),
        },
        {
            "title": "Yangi brieflar",
            "value": ContactRequest.objects.filter(status=ContactRequest.Status.NEW).count(),
            "hint": f"30 kunda: {ContactRequest.objects.filter(created_at__gte=month_ago).count()} ta",
            "icon": "mail",
            "href": reverse("admin:core_contactrequest_changelist") + "?status__exact=new",
        },
    ]

    quick = [
        {"title": "Yangi maqola yozish", "icon": "edit_square", "href": reverse("admin:blog_post_add")},
        {"title": "Loyiha qo'shish", "icon": "add_photo_alternate", "href": reverse("admin:portfolio_project_add")},
        {"title": "Sayt sozlamalari", "icon": "tune", "href": reverse("admin:core_sitesettings_changelist")},
    ]

    context.update({
        "dash_cards": cards,
        "dash_quick": quick,
        "dash_requests": ContactRequest.objects.order_by("-created_at")[:6],
        "dash_drafts": posts.filter(status=Post.Status.DRAFT).order_by("-updated_at")[:6],
        "dash_top_posts": posts.filter(status=Post.Status.PUBLISHED).order_by("-views")[:5],
    })
    return context
