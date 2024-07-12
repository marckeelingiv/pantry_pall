from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CookbookViewSet

router = DefaultRouter()
router.register(r'cookbooks', CookbookViewSet, basename='cookbook')

urlpatterns = [
    path('', include(router.urls)),
]
