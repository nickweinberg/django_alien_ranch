# ajax.py
from .models import Player, Game, Day
import json
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax


@dajaxice_register
def add_player_to_game(request, game_id, user):

    return json.dumps(
        {
            'message': game_id,
            'user': user
        }
    )