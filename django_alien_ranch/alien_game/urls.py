from django.conf.urls import patterns, include, url
from .views import GameListView, GameCreateView, GameLobbyView, MainGameView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Game Index
    url(r'^$', GameListView.as_view(), name='game_home'),
    url(r'^new/$', GameCreateView.as_view(), name='new_game'),
    url(r'^(?P<pk>\d+)/$', GameLobbyView, name='lobby'),
    # dajaxice URLS
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    url(r'^(?P<pk>\d+)/(?P<current_day>\d+)/$', MainGameView, name='play')

) 

urlpatterns += staticfiles_urlpatterns()

