from collections import OrderedDict
from rest_framework import serializers
from .models import Tune
from ..performance.models import Performance
from ..room.models import Room


class TuneCreateSerializer(serializers.ModelSerializer):

    response_data = None
    player_id_set = serializers.ListField(required=False)
    room_id = serializers.UUIDField(required=False)

    class Meta:
        model = Tune
        fields = ('id', 'name', 'room_id', 'status', 'playing_key', 'player_id_set')

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    def validate_player_id_set(self, player_id_set):
        return player_id_set

    # =========================================================
    # write methods define custom query below.
    # =========================================================

    def create(self, *args, **kwargs):
        request_data = OrderedDict(
            name=self.validated_data.get('name'),
            room_id=kwargs['room_id'],
        )
        instance = self.__create_tune(request_data)
        request_data.update(
            id=instance.id,
            status=instance.status,
            playing_key=instance.playing_key,
            player_id_set=self.initial_data.get('player_id_set')
        )
        request_data.move_to_end('id', False)
        self.__create_performance(request_data)
        request_data.update(
            status=instance.get_status_display(),
            playing_key=instance.get_playing_key_display()
        )
        self.response_data = request_data
        return instance

    def __create_tune(self, request_data):
        formatted_data = dict(
            name=request_data.get('name'),
            room_id=request_data.get('room_id')
        )
        return Tune.objects.create(**formatted_data)

    def __create_performance(self, request_data):
        formatted_data = list(map(lambda x: Performance(
            player_id=x,
            tune_id=request_data.get('id'),
            room_id=request_data.get('room_id')
        ), request_data.get('player_id_set')))
        return Performance.objects.bulk_create(formatted_data)


class TuneReadSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(
        choices=Tune.STATUS,
        source='get_status_display'
    )
    playing_key = serializers.ChoiceField(
        choices=Tune.PLAYING_KEY,
        source='get_playing_key_display'
    )
    player_id_set = serializers.SerializerMethodField(
        source='get_player_id_set'
    )

    class Meta:
        model = Tune
        fields = ('id', 'name', 'status', 'playing_key', 'player_id_set')

    def get_player_id_set(self, obj):
        conditions = dict([('tune_id', obj.id), ('room_id', obj.room_id)])
        instance = Performance.objects.filter(**conditions)
        return [x.player_id for x in instance]


class TuneUpdateSerializer(serializers.ModelSerializer):

    response_data = None
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    playing_key = serializers.IntegerField(required=False)
    room_id = serializers.UUIDField(required=False)
    performed_players = serializers.ListField(required=False)

    class Meta:
        model = Tune
        fields = ('id', 'name', 'status', 'playing_key',
                  'room_id', 'performed_players')

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    def validate_room_id(self, room_id):
        if room_id not in [data.id for data in Room.objects.all()]:
            raise self.ValidationError('room_id does not exist in database.')
        return room_id

    # =========================================================
    # write methods define custom query below.
    # =========================================================

    def update(self, *args, **kwargs):
        request_data = OrderedDict(
            id=self.data.get('id'),
            room_id=kwargs['room_id']
        )
        for attr, value in self.validated_data.items():
            if value:
                request_data.update([(attr, value)])

        instance = self.__update_tune(self.instance, request_data)

        if request_data.get('player_id_set'):
            self.__delete_performance(request_data)
            self.__create_performance(request_data)

        if request_data.get('status'):
            request_data.update(
                status=instance.get_status_display(),
            )

        if request_data.get('playing_key'):
            request_data.update(
                playing_key=instance.get_playing_key_display()
            )

        self.response_data = request_data

        return instance

    def __update_tune(self, instance, request_data):

        formatted_data = {}
        for attr, value in request_data.items():
            if value:
                formatted_data.update([(attr, value)])
        for attr, value in formatted_data.items():
            setattr(instance, attr, value)
        instance.save()

        return formatted_data

    def __delete_performance(self, request_data):
        formatted_data = dict(
            tune_id=request_data.get('id'),
            room_id=request_data.get('room_id')
        )
        return Performance.objects.filter(**formatted_data).delete()

    def __create_performance(self, request_data):
        formatted_data = list(map(lambda x: Performance(
            player_id=x,
            tune_id=request_data.get('id'),
            room_id=request_data.get('room_id')
        ), request_data.get('player_id_set')))
        return Performance.objects.bulk_create(formatted_data)


class TuneDeleteSerializer(serializers.ModelSerializer):

    response_data = None
    id = serializers.UUIDField(required=True)
    room_id = serializers.UUIDField(required=False)

    class Meta:
        model = Tune
        fields = ('id',)

    # =========================================================
    # write methods define custom field validation below.
    # =========================================================

    def validate_room_id(self, room_id):
        if room_id not in [data.id for data in Room.objects.all()]:
            raise self.ValidationError('room_id does not exist in database.')
        return room_id

    # =========================================================
    # write methods define custom query below.
    # =========================================================

    def delete(self, *args, **kwargs):
        request_data = OrderedDict(
            room_id=kwargs('room_id'),
        )
        instance = self.__delete_tune(request_data)
        self.__delete_performance(request_data)
        self.response_data = request_data
        return instance

    def __delete_tune(self, request_data):
        formatted_data = dict(
            id=self.request_data.get('id'),
            room_id=request_data.get('room_id')
        )
        return Tune.objects.filter(**formatted_data).delete()

    def __delete_performance(self, request_data):
        formatted_data = dict(
            tune_id=self.request_data.get('id'),
            room_id=request_data.get('room_id')
        )
        return Performance.objects.filter(**formatted_data).delete()
