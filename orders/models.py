import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1
        CONFIRMED = 2
        PAID = 3
        CANCELLED = -1

    status = models.IntegerField(choices=Status, default=1)
    key = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='users_order', on_delete=models.CASCADE
    )
    games = models.ManyToManyField('games.Game', related_name='game_orders', blank=True)

    @property
    def price(self):
        return sum(game.price for game in self.price.all())

    # def __str__(self):
    #     return self.key
