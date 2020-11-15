from common.router import NestedDefaultRouter
from .views import PlayerViewSet
from application.room.urls import room_router

player_router = NestedDefaultRouter(room_router, r'rooms', lookup='room')
player_router.register(r'players', PlayerViewSet)
