from django.conf.urls import patterns, include, url
from django_alien_ranch.views import HomePageView

urlpatterns = patterns('',
    # Game Index
    url(r'^$', HomePageView.as_view(), name='home') #placeholder

)

