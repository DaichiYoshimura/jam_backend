from django.db import models
from uuid import uuid4


class Tune(models.Model):

    PLAYING_KEY = (
        (0, "unassigned"),
        (1, "C"),
        (2, "D♭"),
        (3, "D"),
        (4, "E♭"),
        (5, "E"),
        (6, "F"),
        (7, "G♭"),
        (8, "G"),
        (9, "A♭"),
        (10, "A"),
        (11, "B♭"),
        (12, "B")
    )
    STATUS = (
        (0, "notyet"),
        (1, "next"),
        (2, "completed")
    )

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=32,
        null=False
    )
    playing_key = models.IntegerField(
        default=0,
        choices=PLAYING_KEY
    )
    status = models.IntegerField(
        default=0,
        choices=STATUS
    )
    room_id = models.UUIDField(
        null=False
    )
