import os
import django
from django.db.models import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions

def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    players = None
    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name, country__icontains=search_country)

    elif search_name is not None and search_country is None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name)

    elif search_name is None and search_country is not None:
        players = TennisPlayer.objects.filter(country__icontains=search_country)

    if not players:
        return ""

    players = players.order_by('ranking')

    result = []
    for player in players:
        result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")
    return '\n'.join(result)


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()
    if not top_player:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins_count} wins."


def get_tennis_player_by_matches_count():
    top_player = TennisPlayer.objects.annotate(matches_played=Count('match_players')).order_by('-matches_played',
                                                                                               'ranking').first()

    if not top_player or top_player.matches_played == 0:
        return ""

    return f"Tennis Player: {top_player.full_name} with {top_player.matches_played} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = (Tournament.objects.prefetch_related('match_tournament')
                   .annotate(matches_count=Count('match_tournament'))
                   .filter(surface_type__icontains=surface)
                   .order_by('-start_date'))
    if not tournaments:
        return ""

    result = []
    for t in tournaments:
        result.append(f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches_count}")

    return '\n'.join(result)


def get_latest_match_info():
    # last_played_match = Match.objects.prefetch_related('players').order_by('-date_played', '-id').first()
    #
    # if last_played_match is None:
    #     return ""
    #
    # players = last_played_match.players.order_by('full_name')
    # player1_full_name = players.first().full_name
    # player2_full_name = players.last().full_name
    #
    # return (f"Latest match played on: {last_played_match.date_played}, "
    #         f"tournament: {last_played_match.tournament__name}, "
    #         f"score: {last_played_match.score}, "
    #         f"players: {player1_full_name} vs {player2_full_name}, "
    #         f"winner: {'TBA' if last_played_match.winner is None else last_played_match.winner__full_name}, "
    #         f"summary: {last_played_match.summary}")

    latest_match = Match.objects \
        .prefetch_related('players') \
        .order_by('-date_played', '-id') \
        .first()

    if latest_match is None:
        return ""

    players = latest_match.players.order_by('full_name')
    player1_full_name = players.first().full_name
    player2_full_name = players.last().full_name
    winner_full_name = "TBA" if latest_match.winner is None else latest_match.winner.full_name

    return f"Latest match played on: {latest_match.date_played}, tournament: {latest_match.tournament.name}, " \
           f"score: {latest_match.score}, players: {player1_full_name} vs {player2_full_name}, " \
           f"winner: {winner_full_name}, summary: {latest_match.summary}"


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.select_related('tournament', 'winner').filter(
        tournament__name__exact=tournament_name).order_by('-date_played')

    if not matches:
        return "No matches found."

    result = []
    for match in matches:
        result.append(
            f"Match played on: {match.date_played}, score: {match.score}, winner: {'TBA' if not match.winner else match.winner.full_name}")
    return '\n'.join(result)


print(get_latest_match_info())
