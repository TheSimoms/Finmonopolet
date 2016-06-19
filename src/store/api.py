from rest_framework import serializers, viewsets, pagination
from rest_framework.response import Response

from finmonopolet.api import SharedAPIRootRouter
from store.models import Store, StoreCategory


class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCategory
        fields = ('id', 'name', )


class StoreListPagination(pagination.PageNumberPagination):
    page_size = 6


class StoreSerializer(serializers.ModelSerializer):
    category = StoreCategorySerializer()

    class Meta:
        model = Store
        fields = '__all__'


class StoreListSerializer(StoreSerializer):
    class Meta(StoreSerializer.Meta):
        fields = ('id', 'name', 'address', 'zip_code', 'postal', 'opening_times', 'opening_times_next', )


class StoreLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'latitude', 'longitude', )


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()

    pagination_class = StoreListPagination

    ordering_fields = ('canonical_name', 'zip_code', 'postal', )
    search_fields = (
        'canonical_name', 'address', 'zip_code', 'postal',
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        elif self.action == 'retrieve':
            return StoreSerializer
        else:
            return StoreListSerializer


class StoreLocationViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Store.objects.all()
        serializer = StoreLocationSerializer(queryset, many=True)

        return Response(serializer.data)


SharedAPIRootRouter().register(r'stores/information', StoreViewSet, base_name='store_information')
SharedAPIRootRouter().register(r'stores/locations', StoreLocationViewSet, base_name='store_locations')
