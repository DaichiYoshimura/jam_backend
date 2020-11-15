from common.router import NestedDefaultRouter
from .views import PerformanceViewSet
from application.room.urls import room_router

performance_router = NestedDefaultRouter(room_router, r'rooms', lookup='room')
performance_router.register(r'performance', PerformanceViewSet)
