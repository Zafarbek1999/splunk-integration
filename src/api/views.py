from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from src.api.serializers import ProductSerializer
from src.core.models import Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny, )
    http_method_names = ('get', 'post', 'put', 'delete')
