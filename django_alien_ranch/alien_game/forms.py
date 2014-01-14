from django import forms
from .models import Game, Vote



class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        # should exclude has_started but testing
        exclude = ('archive', 'users', 'winner')

class GameVoteForm(forms.ModelForm):
    # Just a stub not sure if i'll use this
    class Meta:
        model = Vote

        exclude = ('day', 'vote_time', 'player_voted')