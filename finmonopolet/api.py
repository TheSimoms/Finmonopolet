from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets, routers, response

from product.models import Country, Producer, Suits
from category.models import Category


class SharedAPIRootRouter(routers.SimpleRouter):
    shared_router = routers.DefaultRouter(trailing_slash=False)

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)

        super().register(*args, **kwargs)


class ForeignKeySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ForeignKeyListSerializer(ForeignKeySerializer):
    number_of_products = serializers.IntegerField()


class ForeignKeyViewSet(viewsets.ViewSet):
    pagination_class = None

    ordering_fields = ('canonical_name', 'number_of_products', )
    search_fields = ('canonical_name', )

    # FIXME: Un-hack this. Probably change to class method
    @staticmethod
    def get_model(request, pk=False):
        model_name = request.path.split('/')[-2 if pk else -1]

        if model_name == 'categories':
            return Category
        elif model_name == 'countries':
            return Country
        elif model_name == 'producers':
            return Producer
        elif model_name == 'suits':
            return Suits

    def list(self, request):
        queryset = self.get_model(request).objects.annotate(
            number_of_products=Count('products'),
        ).filter(
            number_of_products__gt=0
        )

        serializer = ForeignKeyListSerializer(queryset, many=True)

        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_model(request, pk=True).objects.all()

        item = get_object_or_404(queryset, pk=pk)

        serializer = ForeignKeySerializer(item)

        return response.Response(serializer.data)
