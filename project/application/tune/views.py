from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Tune
from .serializer import TuneCreateSerializer
from .serializer import TuneReadSerializer
from .serializer import TuneUpdateSerializer
from .serializer import TuneDeleteSerializer


class TuneFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='exact')

    class Meta:
        model = Tune
        fields = ('id', 'name', 'room_id')


class TuneViewSet(viewsets.ModelViewSet):

    queryset = Tune.objects.all()
    serializer_class = TuneReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TuneFilter

    def get_queryset(self):
        queryset = Tune.objects.filter(room_id=self.kwargs['room_pk'])
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TuneReadSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return TuneUpdateSerializer
        if self.request.method == 'DELETE':
            return TuneDeleteSerializer
        return TuneCreateSerializer

    # ===========================================================
    # write override methods perform serializer and query below.
    # ===========================================================

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(room_id=self.kwargs['room_pk'])
        return Response(
            data=serializer.response_data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(room_id=self.kwargs['room_pk'])
        return Response(
            data=serializer.response_data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete(room_id=self.kwargs['room_pk'])
        return Response(
            data=serializer.response_data,
            status=status.HTTP_200_OK,
        )
