import re

from rest_framework import serializers

from .models import (
    Client, ContactRequest, Experience, Service, SiteSettings, Technology, Testimonial,
)


class MediaUrlField(serializers.FileField):
    """Fayl URL'ini nisbiy (/media/...) ko'rinishda qaytaradi — frontend bilan bir domenda ishlaydi."""

    def to_representation(self, value):
        if not value:
            return None
        try:
            return value.url
        except ValueError:
            return None


class SiteSettingsSerializer(serializers.ModelSerializer):
    avatar = MediaUrlField(read_only=True)
    about_photo = MediaUrlField(read_only=True)
    cv_file = MediaUrlField(read_only=True)
    og_image = MediaUrlField(read_only=True)

    class Meta:
        model = SiteSettings
        exclude = ["id"]


class TechnologySerializer(serializers.ModelSerializer):
    icon = MediaUrlField(read_only=True)
    group_label = serializers.CharField(source="get_group_display", read_only=True)

    class Meta:
        model = Technology
        fields = ["id", "name", "group", "group_label", "icon", "color"]


class ServiceSerializer(serializers.ModelSerializer):
    features = serializers.ListField(source="feature_list", read_only=True)

    class Meta:
        model = Service
        fields = ["id", "title", "short", "icon", "features", "price_from"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ["id", "company", "position", "period", "description", "url"]


class ClientSerializer(serializers.ModelSerializer):
    logo = MediaUrlField(read_only=True)

    class Meta:
        model = Client
        fields = ["id", "name", "logo", "url"]


class TestimonialSerializer(serializers.ModelSerializer):
    avatar = MediaUrlField(read_only=True)

    class Meta:
        model = Testimonial
        fields = ["id", "author", "position", "avatar", "text", "rating"]


class ContactRequestSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Service.objects.filter(is_active=True),
    )
    # Bot'lar uchun tuzoq: haqiqiy foydalanuvchi bu maydonni ko'rmaydi
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = ContactRequest
        fields = ["name", "phone", "email", "company", "services", "budget", "message", "website"]

    def validate_phone(self, value):
        digits = re.sub(r"\D", "", value)
        if len(digits) < 9:
            raise serializers.ValidationError("Telefon raqamni to'liq kiriting")
        return value.strip()

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Ismingizni kiriting")
        return value

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)
