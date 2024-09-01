import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Review, Article
from django.db.models import Count, Avg


# Create queries within functions


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(full_name__icontains=search_name, email__icontains=search_email).order_by(
            '-full_name')

    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name).order_by('-full_name')

    elif search_email is not None:
        authors = Author.objects.filter(email__icontains=search_email).order_by('-full_name')

    if not authors:
        return ""

    result = []

    for a in authors:
        result.append(f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}")

    return '\n'.join(result)


def get_top_publisher():
    top_publisher = Author.objects.get_authors_by_article_count().filter(articles_count__gt=0).first()

    if not top_publisher or top_publisher.articles_count == 0:
        return ""

    return f"Top Author: {top_publisher.full_name} with {top_publisher.articles_count} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(reviews_count=Count('authors')).order_by('-reviews_count', 'email').first()

    if not top_reviewer or top_reviewer.reviews_count == 0:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews."


def get_latest_article():
    latest_article = Article.objects.prefetch_related('authors', 'articles').order_by('-published_on').first()

    if not latest_article:
        return ""
    authors_names = ', '.join([a.full_name for a in latest_article.authors.all().order_by('full_name')])
    reviews_count = latest_article.articles.count()
    avg_review = sum(r.rating for r in latest_article.articles.all()) / reviews_count if reviews_count else 0

    return (f"The latest article is: {latest_article.title}. "
            f"Authors: {authors_names}. "
            f"Reviewed: {reviews_count} times. "
            f"Average Rating: {avg_review:.2f}.")


def get_top_rated_article():
    top_article = Article.objects.annotate(avg_rating=Avg('articles__rating')).order_by('-avg_rating', 'title').first()
    reviews_count = top_article.articles.count() if top_article else 0

    if not top_article or reviews_count == 0:
        return ""

    return (f"The top-rated article is: {top_article.title}, "
            f"with an average rating of {top_article.avg_rating:.2f}, "
            f"reviewed {reviews_count} times.")


def ban_author(email=None):
    author = Author.objects.prefetch_related('authors').filter(email__exact=email).first()

    if not author or email is None:
        return "No authors banned."

    reviews_count = author.authors.count()
    author.is_banned = True
    author.authors.all().delete()
    author.save()

    return f"Author: {author.full_name} is banned! {reviews_count} reviews deleted."
