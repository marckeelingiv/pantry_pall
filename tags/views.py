from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Tag
from .serializers import TagSerializer

class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return request.user.is_staff
        return super().has_permission(request, view)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
