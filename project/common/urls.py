from django.contrib import admin
from django.conf.urls import url, include

from common.router import CustomRouter
from application.performance.urls import performance_router
from application.player.urls import player_router
from application.tune.urls import tune_router
from application.room.urls import room_router

"""
router = CustomRouter()
router.extend(performance_router)
router.extend(tune_router)
"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(room_router.urls)),
    url(r'^api/', include(player_router.urls)),
    url(r'^api/', include(performance_router.urls)),
    url(r'^api/', include(tune_router.urls)),
]
