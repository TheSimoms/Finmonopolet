from django.db.models import Count

from rest_framework import serializers, viewsets, routers, pagination

from product.models import Category, Country, Producer, Suits


class SharedAPIRootRouter(routers.SimpleRouter):
    shared_router = routers.DefaultRouter(trailing_slash=False)

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)

        super().register(*args, **kwargs)


class ForeignKeyPagination(pagination.PageNumberPagination):
    page_size = 5


class ForeignKeySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ForeignKeyListSerializer(ForeignKeySerializer):
    number_of_products = serializers.IntegerField()


class ForeignKeyViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = ForeignKeyPagination

    ordering_fields = ('canonical_name', )
    search_fields = ('canonical_name', )

    def get_queryset(self):
        model_name = self.request.path.split('/')[2]

        if model_name == 'categories':
            queryset = Category
        elif model_name == 'countries':
            queryset = Country
        elif model_name == 'producers':
            queryset = Producer
        elif model_name == 'suits':
            queryset = Suits
        else:
            return

        return queryset.objects.annotate(
            number_of_products=Count('products'),
        ).filter(
            number_of_products__gt=0
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ForeignKeyListSerializer
        elif self.action == 'retrieve':
            return ForeignKeySerializer
        else:
            return ForeignKeySerializer
