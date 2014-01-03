from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import UserProfileDetailView, HomePageView
admin.autodiscover()

urlpatterns = patterns('',

    # HOME PAGE
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    
    # URLS for Account Registration *django-registration*
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    # User Profile View
    url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name='profile'),


)
