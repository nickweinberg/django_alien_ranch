from django.conf.urls import patterns, include, url
from .views import GameListView, GameCreateView, GameLobbyView

urlpatterns = patterns('',
    # Game Index
    url(r'^$', GameListView.as_view(), name='game_home'),
    url(r'^new/$', GameCreateView.as_view(), name='new_game'),
    url(r'^(?P<pk>\d+)/$', GameLobbyView.as_view(), name='lobby'),

)

