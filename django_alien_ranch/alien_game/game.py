from .models import Player, Game, Day

from random import randint

def start_game(game_id):
    # create a new day
    game = get_object_or_404(Game, pk=game_id)
    new_day = Day(game=game, current_state='morning')

    # add a role to each player IN THE Game
    player_list = game.players.all()

    return 
