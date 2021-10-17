from rest_framework import serializers

from authorization.auth_seriallizers import UserSerializer
from ccg.models import Room, RoomPlayer, Player


class PlayerSerializers(serializers.ModelSerializer):
    User = UserSerializer()

    class Meta:
        model = Player
        fields = ['User', 'classPlayer', 'coins']


class RoomPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializers()

    class Meta:
        model = RoomPlayer
        fields = ['player']


class RoomSerializer(serializers.ModelSerializer):
    players = RoomPlayerSerializer(many=True)

    class Meta:
        model = Room
        fields = ['name', 'players']


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name']
