from django.db import models
from uuid import uuid4


class Player(models.Model):

    STATUS = (
        (1, "participating"),
        (2, "breaking"),
        (3, "left"),
    )

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=32,
        null=False,
    )
    part = models.CharField(
        max_length=32,
        null=False,
    )
    status = models.IntegerField(
        default=1,
        choices=STATUS,
    )
    room_id = models.UUIDField(
        null=False,
    )
