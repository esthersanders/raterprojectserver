"""Game Picture model module"""
from django.db import models
from django.contrib.auth.models import User


class GamePicture(models.Model):
    """Game Picture database model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    picture = models.CharField(max_length=256)