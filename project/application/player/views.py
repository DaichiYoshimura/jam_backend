from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import Player
from .serializer import PlayerReadSerializer, PlayerWriteSerializer
from application.performance.models import Performance
from django.db.models.query import QuerySet


class PlayerFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='exact')

    class Meta:
        model = Player
        fields = ['id', 'name', 'part', 'status']


class PlayerViewSet(viewsets.ModelViewSet):

    queryset = Player.objects.none()
    serializer_class = PlayerReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlayerFilter

    def get_queryset(self):
        queryset = Player.objects.filter(room_id=self.kwargs['room_pk'])
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlayerReadSerializer
        return PlayerWriteSerializer

    # ===========================================================
    # write override methods perform serializer and query below.
    # ===========================================================
    def perform_create(self, serializer):
        serializer.save(room_id=self.kwargs['room_pk'])

    def perform_destroy(self, instance):
        Performance.objects.filter(
            player_id=self.kwargs['pk'], room_id=self.kwargs['room_pk']).delete()
        instance.delete()
