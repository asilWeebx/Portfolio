from rest_framework import serializers

from core.serializers import MediaUrlField, TechnologySerializer

from .models import Project, ProjectCategory, ProjectImage


class ProjectCategorySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = ProjectCategory
        fields = ["id", "name", "slug", "count"]


class ProjectImageSerializer(serializers.ModelSerializer):
    image = MediaUrlField(read_only=True)
    w = serializers.SerializerMethodField()
    h = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ["id", "image", "caption", "w", "h"]

    def get_w(self, obj):
        try:
            return obj.image.width
        except Exception:
            return None

    def get_h(self, obj):
        try:
            return obj.image.height
        except Exception:
            return None


class ProjectListSerializer(serializers.ModelSerializer):
    cover = MediaUrlField(read_only=True)
    logo = MediaUrlField(read_only=True)
    category = ProjectCategorySerializer(read_only=True)
    technologies = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    platforms = serializers.ListField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "title", "slug", "category", "short_description", "cover",
            "accent_color", "year", "client", "technologies", "is_featured", "platforms", "logo",
        ]


class ProjectNavSerializer(serializers.ModelSerializer):
    cover = MediaUrlField(read_only=True)

    class Meta:
        model = Project
        fields = ["title", "slug", "cover"]


class ProjectDetailSerializer(ProjectListSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    prev = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()

    class Meta(ProjectListSerializer.Meta):
        fields = ProjectListSerializer.Meta.fields + [
            "content", "role", "duration", "live_url", "github_url", "app_store_url",
            "play_store_url", "telegram_url", "desktop_url", "images", "seo_title", "seo_description",
            "prev", "next",
        ]

    def _neighbours(self, obj):
        if not hasattr(self, "_nb"):
            ids = list(
                Project.objects.filter(is_published=True)
                .order_by(*Project._meta.ordering).values_list("id", flat=True)
            )
            i = ids.index(obj.id) if obj.id in ids else -1
            prev_id = ids[i - 1] if i > 0 else None
            next_id = ids[i + 1] if 0 <= i < len(ids) - 1 else None
            self._nb = {
                p.id: p for p in Project.objects.filter(id__in=[x for x in (prev_id, next_id) if x])
            }
            self._nb_ids = (prev_id, next_id)
        return self._nb, self._nb_ids

    def get_prev(self, obj):
        nb, (prev_id, _) = self._neighbours(obj)
        return ProjectNavSerializer(nb[prev_id]).data if prev_id else None

    def get_next(self, obj):
        nb, (_, next_id) = self._neighbours(obj)
        return ProjectNavSerializer(nb[next_id]).data if next_id else None
