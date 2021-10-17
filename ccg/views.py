from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ccg.css_serializers import CreateRoomSerializer, RoomSerializer, PlayerSerializers
from ccg.models import Room, RoomPlayer, Player


class RoomCreate(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        room = serializer.save(name=self.request.data['name'])
        RoomPlayer.objects.create(room=room, player_id=self.request.data['player'], deck_id=self.request.data['deck'])


class ConnectRoom(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        room = Room.objects.get(name=request.data['room'])
        player = RoomPlayer.objects.create(room=room, player_id=request.data['player']
                                           , deck_id=request.data['deck'])
        return Response('created')


class RoomRetrieve(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'name'


class PlayerRetrieve(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializers
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'User_id'


class RoomDestroy(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'name'
