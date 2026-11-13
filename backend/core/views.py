import logging

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostListSerializer
from portfolio.models import Project
from portfolio.serializers import ProjectListSerializer

from .models import (
    Client, ContactRequest, Experience, Service, SiteSettings, Technology, Testimonial,
)
from .notify import notify_new_request
from .serializers import (
    ClientSerializer, ContactRequestSerializer, ExperienceSerializer, ServiceSerializer,
    SiteSettingsSerializer, TechnologySerializer, TestimonialSerializer,
)

log = logging.getLogger(__name__)


class SiteView(APIView):
    """Har bir sahifada kerak bo'ladigan umumiy ma'lumot (header, footer, brief formasi)."""

    def get(self, request):
        return Response({
            "settings": SiteSettingsSerializer(SiteSettings.load()).data,
            "services": ServiceSerializer(Service.objects.filter(is_active=True), many=True).data,
        })


class HomeView(APIView):
    """Bosh sahifa uchun barcha bloklar bitta so'rovda."""

    def get(self, request):
        s = SiteSettings.load()
        projects = (
            Project.objects.filter(is_published=True)
            .select_related("category").prefetch_related("technologies")
        )
        featured = projects.filter(is_featured=True)[:10] or projects[:10]
        posts = (
            Post.published.select_related("category").prefetch_related("tags")[:4]
        )
        return Response({
            "technologies": TechnologySerializer(
                Technology.objects.filter(is_active=True, show_on_home=True), many=True,
            ).data,
            "experience": ExperienceSerializer(Experience.objects.filter(is_active=True), many=True).data,
            "testimonials": TestimonialSerializer(Testimonial.objects.filter(is_active=True), many=True).data,
            "clients": ClientSerializer(Client.objects.filter(is_active=True), many=True).data,
            "featured_projects": ProjectListSerializer(featured, many=True).data,
            "latest_posts": PostListSerializer(posts, many=True).data,
            "stats": {
                "years": s.years_experience,
                "projects": projects.count(),
                "clients": s.happy_clients,
                "posts": Post.published.count(),
            },
        })


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactRequestSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Honeypot to'ldirilgan bo'lsa — jim "muvaffaqiyat" qaytaramiz, bazaga yozmaymiz
        if serializer.validated_data.get("website"):
            return Response({"ok": True}, status=status.HTTP_201_CREATED)
        ip = (request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR") or "").split(",")[0].strip()
        obj: ContactRequest = serializer.save(ip=ip or None)
        try:
            notify_new_request(obj)
        except Exception:  # xabar yuborilmasa ham so'rov saqlanib qoladi
            log.exception("Telegram xabarini yuborib bo'lmadi")
        return Response({"ok": True}, status=status.HTTP_201_CREATED)
