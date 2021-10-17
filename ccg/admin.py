from django.contrib import admin

from ccg.models import Card, ClassPlayer, Player, CardType, Deck, DeckCard, CardCollection, Room, RoomPlayer

admin.site.register(Card)
admin.site.register(ClassPlayer)
admin.site.register(Player)
admin.site.register(CardType)
admin.site.register(Deck)
admin.site.register(DeckCard)
admin.site.register(CardCollection)
admin.site.register(Room)
admin.site.register(RoomPlayer)
