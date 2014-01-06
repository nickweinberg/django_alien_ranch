from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.shortcuts import render

from .models import Player, Game, Day
from .forms import GameCreateForm

from django.contrib.auth.models import User


class GameListView(ListView):
    model = Game


class GameCreateView(CreateView):
    model = Game
    form_class = GameCreateForm

class GameLobbyView(DetailView):
    model = Game
