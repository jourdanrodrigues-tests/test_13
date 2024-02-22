from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from app import views

docs_view = get_schema_view(
    openapi.Info(title="Aktos Exercise API", default_version="v1"),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r"consumers", views.ConsumerViewSet)

urlpatterns = [
    path("", include(router.urls)),  # I'd rather have it under an "/api" domain but I'm gonna stick to the document
    path("admin/", admin.site.urls),
    path("docs/", docs_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
