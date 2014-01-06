from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_alien_ranch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^game/', 'alien_game.views.game_view'),

    url(r'^api01/chat/send/', 'alien_game.views.game_chat_send'),
    url(r'^api01/chat/ping/', 'alien_game.views.game_chat_ping'),

    url(r'^admin/', include(admin.site.urls)),
)
