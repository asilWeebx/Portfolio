from django.urls import path

from .views import ProjectCategoryListView, ProjectDetailView, ProjectListView

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="api-projects"),
    path("projects/categories/", ProjectCategoryListView.as_view(), name="api-project-categories"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="api-project-detail"),
]
