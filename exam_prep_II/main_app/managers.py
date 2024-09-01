from django.db import models
from django.db.models import Count


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return self.annotate(order_numbers=Count('orders')).filter(order_numbers__gt=2).order_by('-order_numbers')
