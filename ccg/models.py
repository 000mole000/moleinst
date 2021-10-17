from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class ClassPlayer(models.Model):
    id = models.CharField(max_length=16, primary_key=True, unique=True)
    name = models.CharField(max_length=32)


class CardType(models.Model):
    id = models.CharField(max_length=16, primary_key=True, unique=True)
    name = models.CharField(max_length=32)


class Player(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    classPlayer = models.ForeignKey(ClassPlayer, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)


class Card(models.Model):
    rarity_choices = [
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ]

    id = models.CharField(max_length=16, primary_key=True, unique=True)
    name = models.CharField(max_length=32)
    text = models.TextField()
    type = models.ForeignKey(CardType, on_delete=models.CASCADE, null=True, blank=True)
    classPlayer = models.ForeignKey(ClassPlayer, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='cards', null=True, blank=True)
    dmg = models.PositiveIntegerField(default=0)
    hp = models.PositiveIntegerField(default=0)
    mana = models.PositiveIntegerField(default=0)
    stamina = models.PositiveIntegerField(default=0)
    max_stamina = models.PositiveIntegerField(default=1)
    rarity = models.CharField(choices=rarity_choices, default='common', max_length=16)


class Deck(models.Model):
    name = models.CharField(max_length=32)
    classPlayer = models.ForeignKey(ClassPlayer, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class CardCollection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        card_collection = CardCollection.objects.filter(card=self.card, player=self.player)
        if card_collection.exists():
            raise ValidationError('This player already have this card')
        else:
            super().save(*args, **kwargs)


class DeckCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')

    def save(self, *args, **kwargs):
        card_collection = CardCollection.objects.filter(card=self.card, player=self.deck.player)
        if card_collection.exists() and \
                (self.deck.classPlayer == self.card.classPlayer or self.card.classPlayer is None)\
                and self.deck.cards.count() < 10\
                and DeckCard.objects.filter(card=self.card, deck=self.deck).count() < 2:
            super().save(*args, **kwargs)
        elif self.deck.classPlayer != self.card.classPlayer and self.card.classPlayer is not None:
            raise ValidationError('Class deck and card does not match')
        elif DeckCard.objects.filter(card=self.card, deck=self.deck).count() >= 2:
            raise ValidationError('This deck has too many of these cards')
        elif self.deck.cards.count() >= 10:
            raise ValidationError('This deck has too many cards')
        elif not card_collection.exists():
            raise ValidationError("This player haven't this card")


class Room(models.Model):
    name = models.CharField(max_length=16, unique=True)


class RoomPlayer(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='players')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='rooms')
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='players_in_game')

    def save(self, *args, **kwargs):
        if self.room.players.count()<2:
            super().save(*args, **kwargs)
        else:
            raise ValidationError("Too many players in this room")
