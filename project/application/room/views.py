from rest_framework import viewsets
from .models import Room
from .serializer import RoomReadSerializer, RoomWriteSerializer
from application.performance.models import Performance


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoomReadSerializer
        return RoomWriteSerializer

    # ===========================================================
    # write override methods perform serializer and query below.
    # ===========================================================

    def perform_destroy(self, instance):
        Performance.objects.filter(room_id=self.kwargs['pk']).delete()
        instance.delete()
