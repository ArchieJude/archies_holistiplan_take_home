from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaxFormViewSet

router = DefaultRouter()
router.register(r'tax-forms', TaxFormViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
