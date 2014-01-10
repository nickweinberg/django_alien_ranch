from alien_game.models import Day, Player, Game, Vote, SIDE
from django.contrib.auth.models import User, UserManager
from django.db.models import Count
from django.shortcuts import get_object_or_404
from random import randint, choice

def start_game(game):

    # add a SIDE to each player IN THE Game
    players_list = game.players.all()

    # Give every user a side
    # set everyone to human
    for player in players_list:
        player.side = SIDE[0][0]
        player.save()

    # Pick random guy, make him alien
    alien_guy = choice(players_list)
    alien_guy.side = SIDE[1][0]
    alien_guy.save()

    # Game starts - Create a new Day
    new_day = Day(game=game, current_day=1, current_state='morning') # sets to morning
    new_day.save()

def morning_vote_round_resolve(game, day):
    """ Gets called if 
    did_everyone_vote_day()
    """
    is_no_ties, player_to_be_killed = new_day.count_up_votes('morning')

    if is_no_ties:
        # Set that player to dead
        player_to_be_killed.current_status = 'dead'
        player_to_be_killed.save()
    elif not is_no_ties:
        # There was a tie, no one dies
        pass

    # Check if game is over
    is_game_over = check_game_over()
    if is_game_over:
        print 'game is over'

    # then advance the round
    day.set_to_night()

def night_vote_round_resolve(game, day):
    """ Gets called if
    did_everyone_vote_night()
    """
    is_no_ties, player_to_be_killed = new_day.count_up_votes('night')

    if is_no_ties:
        # Set that player to dead
        player_to_be_killed.current_status = 'dead'
        player_to_be_killed.save()
    elif not is_no_ties:
        # There was a tie, no one dies
        pass

    # Check if game is over
    is_game_over = check_game_over()
    if is_game_over:
        print 'game is over'

    # Make a new instance of day
    night_message = str(player_to_be_killed.user) + " got abducted!"

    another_day = new_day.create_new_day(game, night_message)


