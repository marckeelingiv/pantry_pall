from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeasurementUnitViewSet

router = DefaultRouter()
router.register(r'measurement-units', MeasurementUnitViewSet, basename='measurementunit')

urlpatterns = [
    path('', include(router.urls)),
]
