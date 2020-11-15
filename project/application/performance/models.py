from django.db import models
from uuid import uuid4


class Performance(models.Model):

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name='ID'
    )
    player_id = models.UUIDField(
        null=False,
    )
    tune_id = models.UUIDField(
        null=False,
    )
    room_id = models.UUIDField(
        null=False,
    )
