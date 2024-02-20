from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()
router.register(r"consumers", views.ConsumerViewSet)

urlpatterns = [
    path("/", include(router.urls)),  # I'd rather have it under an "/api" domain but I wanna stick to the document
    path("admin/", admin.site.urls),
]
