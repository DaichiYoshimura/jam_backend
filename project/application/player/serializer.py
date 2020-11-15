from rest_framework import serializers
from .models import Player
from ..performance.models import Performance


class PlayerWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('name', 'part')

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    # =========================================================
    # write methods define custom query below.
    # =========================================================


class PlayerReadSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Player.STATUS, source='get_status_display')
    performed_tunes = serializers.SerializerMethodField(source='get_performed_tunes')

    class Meta:
        model = Player
        fields = ('id', 'name', 'part', 'status', 'performed_tunes', 'room_id')

    def get_performed_tunes(self, obj):
        return [x.tune_id for x in Performance.objects.filter(player_id=obj.id)]

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    # =========================================================
    # write methods define custom query below.
    # =========================================================
