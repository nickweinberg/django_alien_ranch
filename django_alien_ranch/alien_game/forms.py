from django import forms
from .models import Game



class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        # should exclude has_started but testing
        exclude = ('archive', 'users')

