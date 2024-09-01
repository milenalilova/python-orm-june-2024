import os
from datetime import timedelta, date

import django
from django.db.models import Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Book, Author, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Car, \
    Registration


# Create queries within functions

def show_all_authors_with_their_books():
    authors_with_books = []

    authors = Author.objects.all()
    for author in authors:
        # books = Book.objects.filter(author=author)
        # other option

        books = author.book_set.all()
        if books:
            titles = ', '.join([b.title for b in books])
            authors_with_books.append(f"{author.name} has written - {titles}!")
    return '\n'.join(authors_with_books)


def delete_all_authors_without_books():
    # Author.objects.filter(book__isnull=True).delete()
    # other option

    authors = Author.objects.all()
    for author in authors:
        books = author.book_set.all()
        if not books:
            author.delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)

    # Artist.objects.get(name=artist_name).songs.add(Song.objects.get(title=song_title))


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    all_songs = artist.songs.order_by('-id')

    # return Artist.objects.get(name=artist_name).songs.all().order_by("-id")

    return all_songs


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)
    # song.artists.remove(artist) the same


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    return average_rating

    #      OR
    # product = Product.objects.annotate(
    #     average_rating=Avg('reviews__rating'),
    # ).get(name=product_name)
    #
    # return product.average_rating

    #        OR
    # product = Product.objects.get(name=product_name)
    # reviews = product.reviews.all()
    #
    # total_rating = sum(r.rating for r in reviews)  # 5 + 1 => 6
    # average_rating = total_rating / len(reviews)  # 6 / 2 => 3
    #
    # return average_rating

    #           OR
    # product = Product.objects.annotate(
    #     average_rating=Avg('reviews__rating'),
    # ).get(name=product_name)
    #
    # return product.average_rating


def get_reviews_with_high_ratings(threshold: int):
    reviews = Review.objects.filter(rating__gte=threshold)
    return reviews


def get_products_with_no_reviews():
    products = Product.objects.filter(reviews__isnull=True).order_by('-name')
    return products


def delete_products_without_reviews():
    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    expiration_dates = []

    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)
        expiration_dates.append(f"License with number: {license.license_number} expires on {expiration_date}!")

    return '\n'.join(expiration_dates)


def get_drivers_with_expired_licenses(due_date: date):
    expiration_cutoff_date = due_date - timedelta(days=365)
    drivers_with_expired_licenses = Driver.objects.filter(license__issue_date__gt=expiration_cutoff_date)
    return drivers_with_expired_licenses


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(owner__isnull=True).first()
    car.owner = owner

    car.save()

    registration.registration_date = date.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."
