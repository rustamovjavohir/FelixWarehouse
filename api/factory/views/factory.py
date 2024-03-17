from rest_framework.generics import GenericAPIView

from apps.factory.models import Product, ProductMaterial, Warehouse, Material
from api.factory.serializers.factory import ProductSerializer, ProductMaterialSerializer, FactorySerializer
from api.mixins import HandleExceptionMixin
from utils.responses import Response
from services.factory import FactoryService


class FactoryView(HandleExceptionMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = FactorySerializer
    service = FactoryService()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _data = self.service.get_data(serializer.validated_data['product'])
        return Response(_data)
