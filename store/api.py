from rest_framework import serializers, viewsets

from finmonopolet.api import SharedAPIRootRouter
from store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Store
        fields = '__all__'


class StoreListSerializer(StoreSerializer):
    class Meta(StoreSerializer.Meta):
        fields = ('id', 'name', 'address', 'zip_code', 'postal', 'category', 'latitude', 'longitude', 'opening_times', )


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()

    ordering_fields = ('name', 'zip_code', 'postal', 'category', )

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        elif self.action == 'retrieve':
            return StoreSerializer
        else:
            return StoreSerializer


SharedAPIRootRouter().register(r'stores', StoreViewSet)
