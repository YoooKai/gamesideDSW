from colorfield.fields import ColorField
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = ColorField(blank=True, default='#ffffff')

    def __str__(self):
        return self.name
