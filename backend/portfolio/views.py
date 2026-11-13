from django.db.models import Count, Q
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Project, ProjectCategory
from .serializers import ProjectCategorySerializer, ProjectDetailSerializer, ProjectListSerializer


class ProjectFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__slug")
    featured = filters.BooleanFilter(field_name="is_featured")
    tech = filters.CharFilter(field_name="technologies__name", lookup_expr="iexact")

    class Meta:
        model = Project
        fields = ["category", "featured", "tech"]


class BentoPagination(PageNumberPagination):
    page_size = 15  # bento to'r 5 tadan takrorlanadi


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = BentoPagination
    filterset_class = ProjectFilter
    search_fields = ["title", "short_description", "client"]

    def get_queryset(self):
        return (
            Project.objects.filter(is_published=True)
            .select_related("category").prefetch_related("technologies").distinct()
        )


class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Project.objects.filter(is_published=True)
            .select_related("category").prefetch_related("technologies", "images")
        )


class ProjectCategoryListView(generics.ListAPIView):
    serializer_class = ProjectCategorySerializer
    pagination_class = None

    def get_queryset(self):
        return (
            ProjectCategory.objects.filter(is_active=True)
            .annotate(count=Count("projects", filter=Q(projects__is_published=True)))
            .filter(count__gt=0)
        )
