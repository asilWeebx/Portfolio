from django.urls import path

from .views import ContactCreateView, HomeView, SiteView

urlpatterns = [
    path("site/", SiteView.as_view(), name="api-site"),
    path("home/", HomeView.as_view(), name="api-home"),
    path("contact/", ContactCreateView.as_view(), name="api-contact"),
]
