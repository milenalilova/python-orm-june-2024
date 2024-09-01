from django.db import models
from django.db.models import Count


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):
        return self.annotate(wins_count=Count('match_winner')).order_by('-wins_count', 'full_name')
