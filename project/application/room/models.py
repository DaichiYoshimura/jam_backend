from django.db import models
from uuid import uuid4


class Room(models.Model):

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=32
    )
