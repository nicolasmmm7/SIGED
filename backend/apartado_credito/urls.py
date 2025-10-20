from rest_framework import routers
from django.urls import path, include
from .views import ApartadoViewSet, CreditoViewSet, CuotaViewSet

router = routers.DefaultRouter()
router.register(r"apartados", ApartadoViewSet)
router.register(r"creditos", CreditoViewSet)
router.register(r"cuotas", CuotaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
