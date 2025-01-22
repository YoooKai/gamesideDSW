from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 0
        CONFIRMED = 1
        CANCELLED = 2
        PAID = 3

    status = models.IntegerField(choices=Status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='users_order', on_delete=models.CASCADE
    )
    games = models.ManyToManyField('games.Game', related_name='game_orders')

    def __str__(self):
        return self.name
