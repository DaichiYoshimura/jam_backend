from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import Performance
from .serializer import PerformanceWriteSerializer, PerformanceReadSerializer
from django.db.models.query import QuerySet


class PerformanceFilter(filters.FilterSet):

    room_id = filters.CharFilter(field_name='room_id', lookup_expr='exact')

    class Meta:
        model = Performance
        fields = ['id', 'player_id', 'tune_id', 'room_id']


class PerformanceViewSet(viewsets.ModelViewSet):

    queryset = Performance.objects.all()
    serializer_class = PerformanceReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PerformanceFilter

    def get_queryset(self):
        queryset = Performance.objects.filter(room_id=self.kwargs['room_pk'])
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PerformanceReadSerializer
        return PerformanceWriteSerializer

    # ===========================================================
    # write override methods perform serializer and query below.
    # ===========================================================
