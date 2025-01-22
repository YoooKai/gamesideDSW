from colorfield.fields import ColorField
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField()
    description = models.TextField()
    color = ColorField()

    def __str__(self):
        return self.name
