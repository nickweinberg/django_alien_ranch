# ajax.py
from .models import Player, Game, Day
import json
from django.shortcuts import get_object_or_404
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

import game

def add_new_player(request, game_id, user, game):
    new_player = Player(user=request.user, game=game)
    new_player.save()


@dajaxice_register
def add_player_to_game(request, game_id, user):

    game = get_object_or_404(Game, pk=game_id)
    if Player.objects.filter(user=request.user,game=game).exists():
        print "WE ALREADY HAVE THIS DUUDE!"
        return json.dumps(
            {
                'message': game_id,
                'error': 'WE ALREADY HAVE THIS DUDE'
            }
        )
    elif Player.objects.filter(game=game).count() > 4:
        print "Too many players"
        return json.dumps(
            {
                'message': game_id,
                'error': 'Too many players in game.'
            }
        )
    elif Player.objects.filter(game=game).count() == 4:
        add_new_player(request, game_id, user, game)

        url = str(game.pk) + '/1' # game id + current day aka 1
        game.start_game(game)
        return json.dumps(
            {
                'message': game_id,
                'user': user,
                'url': url
            }
        )


    else:
        add_new_player(request, game_id, user, game)
        return json.dumps(
            {
                'message': game_id,
                'user': user
            }
        )



