from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3
        PEGI4 = 4
        PEGI6 = 6
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    pegi = models.IntegerField(choices=Pegi, max_length=2)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField()
    price = models.PositiveSmallIntegerField()
    stock = models.PositiveIntegerField()
    release_at = models.DateField()
    category = models.ForeignKey(
        'categories.Category', related_name='categories', on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    game = models.ForeignKey('games.Game', related_name='games', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='user', on_delete=models.CASCADE)
