from django.db import models
from django.db.models import Count


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        return self.annotate(articles_count=Count('articles_authors')).order_by('-articles_count', 'email')



