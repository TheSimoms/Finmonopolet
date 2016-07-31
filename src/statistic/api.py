from rest_framework import serializers, viewsets
from rest_framework.response import Response

from finmonopolet.api import SharedAPIRootRouter, ForeignKeySerializer

from statistic.models import Statistics


class StatisticSerializer(serializers.ModelSerializer):
    category = ForeignKeySerializer()
    country = ForeignKeySerializer()

    class Meta:
        model = Statistics
        fields = '__all__'


class StatisticViewSet(viewsets.ViewSet):
    def list(self, request):
        filters = {}

        if ('category' in request.GET):
            filters['category__id'] = request.GET['category']
        elif ('country' in request.GET):
            filters['country__id'] = request.GET['country']

        queryset = Statistics.objects.filter(**filters)
        serializer = StatisticSerializer(queryset, many=True, read_only=True)

        return Response(serializer.data)


SharedAPIRootRouter().register(r'statistics', StatisticViewSet, base_name='statistics')
