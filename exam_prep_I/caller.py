import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Director, Actor, Movie
from django.db.models import Q, F, Count, Avg, Max


# Create queries within functions

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query = None
    if search_name is not None and search_nationality is not None:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)
    elif search_name is not None:
        query = Q(full_name__icontains=search_name)
    elif search_nationality is not None:
        query = Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []
    for director in directors:
        result.append(f"Director: {director.full_name}, "
                      f"nationality: {director.nationality}, "
                      f"experience: {director.years_of_experience}")

    return '\n'.join(result)


def get_top_director():
    directors = Director.objects.get_directors_by_movies_count().first()

    if not directors:
        return ""

    return f"Top Director: {directors.full_name}, movies: {directors.movies_count}."


def get_top_actor():
    actor = (Actor.objects.prefetch_related('starring_movies')
             .annotate(
        movies_count=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating')).order_by('-movies_count', 'full_name')).first()

    if not actor:
        return ""

    movies = actor.starring_movies.all()
    if not movies:
        return ""

    result = []
    for movie in movies:
        result.append(movie.title)

    return (f"Top Actor: {actor.full_name}, "
            f"starring in movies: {', '.join(result)}, "
            f"movies average rating: {actor.movies_avg_rating:.1f}")


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(movies_count=Count('actor_movies')).order_by('-movies_count', 'full_name')[:3]

    if not actors or not actors[0].movies_count:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.movies_count} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = (Movie.objects.filter(is_awarded=True)
                 .annotate(highest_rating=Max('rating'))
                 .order_by('title')
                 .first())
    if not top_movie:
        return ""

    lead_actor = top_movie.starring_actor.full_name if top_movie.starring_actor is not None else 'N/A'
    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)

    return (f"Top rated awarded movie: {top_movie.title}, "
            f"rating: {top_movie.rating:.1f}. "
            f"Starring actor: {lead_actor}. "
            f"Cast: {', '.join(participating_actors)}.")


def increase_rating():
    updated_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0).update(rating=F('rating') + 0.1)

    if not updated_movies:
        return "No ratings increased."

    return f"Rating increased for {updated_movies} movies."


