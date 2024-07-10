from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Cookbook
from .serializers import CookbookSerializer
from .permissions import IsAuthorOrReadOnly

class CookbookViewSet(viewsets.ModelViewSet):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
