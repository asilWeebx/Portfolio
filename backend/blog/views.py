from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Post, Tag
from .serializers import CategorySerializer, PostDetailSerializer, PostListSerializer, TagSerializer


def published_q() -> Q:
    return Q(posts__status=Post.Status.PUBLISHED, posts__published_at__lte=timezone.now())


class PostFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__slug")
    tag = filters.CharFilter(field_name="tags__slug")
    featured = filters.BooleanFilter(field_name="is_featured")

    class Meta:
        model = Post
        fields = ["category", "tag", "featured"]


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    filterset_class = PostFilter
    search_fields = ["title", "excerpt", "content", "tags__name"]
    ordering_fields = ["published_at", "views"]

    def get_queryset(self):
        return Post.published.select_related("category").prefetch_related("tags").distinct()


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Post.published.select_related("category").prefetch_related("tags")


class PostViewCounter(APIView):
    """Ko'rishlar sonini oshirish (GET'ni idempotent saqlash uchun alohida POST)."""

    def post(self, request, slug):
        post = get_object_or_404(Post.published, slug=slug)
        Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
        return Response({"views": post.views + 1})


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return Category.objects.annotate(count=Count("posts", filter=published_q(), distinct=True))


class TagListView(generics.ListAPIView):
    serializer_class = TagSerializer
    pagination_class = None

    def get_queryset(self):
        return (
            Tag.objects.annotate(count=Count("posts", filter=published_q(), distinct=True))
            .filter(count__gt=0).order_by("-count", "name")
        )
