from rest_framework import serializers
from .models import Performance
from ..tune.models import Tune
from ..room.models import Room
from ..player.models import Player


class PerformanceWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = ('__all__')

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    def validate_room_id(self, room_id):
        registered_rooms = [data.id for data in Room.objects.all()]
        if room_id not in registered_rooms:
            raise serializers.ValidationError('room_id does not exist in database.')

    def validate_tune_id(self, tune_id):
        registered_tunes = [data.id for data in Tune.objects.all()]
        if tune_id not in registered_tunes:
            raise serializers.ValidationError('tune_id does not exist in database.')

    def validate_player_id(self, player_id):
        registered_players = [data.id for data in Player.objects.all()]
        if player_id not in registered_players:
            raise serializers.ValidationError('player_id does not exist in database.')

    # =========================================================
    # write methods define custom query below.
    # =========================================================


class PerformanceReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = ('__all__')
