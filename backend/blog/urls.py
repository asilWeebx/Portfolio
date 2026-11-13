from django.urls import path

from .views import CategoryListView, PostDetailView, PostListView, PostViewCounter, TagListView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="api-posts"),
    path("posts/categories/", CategoryListView.as_view(), name="api-post-categories"),
    path("posts/tags/", TagListView.as_view(), name="api-post-tags"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="api-post-detail"),
    path("posts/<slug:slug>/view/", PostViewCounter.as_view(), name="api-post-view"),
]
