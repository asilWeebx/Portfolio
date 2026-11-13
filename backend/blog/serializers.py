from rest_framework import serializers

from core.serializers import MediaUrlField

from .models import Category, Post, Tag


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "emoji", "count"]


class TagSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "count"]


class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug", "emoji"]


class TagMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "slug"]


class PostListSerializer(serializers.ModelSerializer):
    cover = MediaUrlField(read_only=True)
    category = CategoryMiniSerializer(read_only=True)
    tags = TagMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "excerpt", "cover", "category", "tags",
            "published_at", "reading_time", "views", "is_featured",
        ]


class PostDetailSerializer(PostListSerializer):
    related = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + [
            "content", "updated_at", "seo_title", "seo_description", "related",
        ]

    def get_related(self, obj):
        qs = Post.published.exclude(pk=obj.pk).select_related("category").prefetch_related("tags")
        same = list(qs.filter(category=obj.category)[:3]) if obj.category_id else []
        if len(same) < 3:
            same += list(qs.exclude(pk__in=[p.pk for p in same])[: 3 - len(same)])
        return PostListSerializer(same, many=True).data
