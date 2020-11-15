from rest_framework import serializers
from .models import Room


class RoomWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('__all__')

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    # =========================================================
    # write methods define custom query below.
    # =========================================================


class RoomReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('__all__')

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    # =========================================================
    # write methods define custom query below.
    # =========================================================
