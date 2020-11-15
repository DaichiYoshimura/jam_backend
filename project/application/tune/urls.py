from common.router import NestedDefaultRouter
from .views import TuneViewSet
from application.room.urls import room_router

tune_router = NestedDefaultRouter(room_router, r'rooms', lookup='room')
tune_router.register(r'tune', TuneViewSet)
