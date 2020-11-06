"""Game model module"""
from raterprojectapi.models import gamecategory
from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    """Game database model"""

    title = models.CharField(max_length=75)
    description = models.CharField(max_length=75)
    designer = models.CharField(max_length=75)
    release_year = models.IntegerField()
    number_of_players = models.IntegerField()
    time = models.IntegerField()
    age = models.IntegerField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)

    @property
    def categories(self):
        game_categories = self.game_categories.all()
        return [ gamecategory.category for gamecategory in game_categories]
