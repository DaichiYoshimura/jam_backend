from common.router import DefaultRouter
from .views import RoomViewSet


room_router = DefaultRouter()
room_router.register(r'rooms', RoomViewSet)
