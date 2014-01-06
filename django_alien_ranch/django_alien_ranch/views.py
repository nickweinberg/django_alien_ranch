from django.views.generic import ListView,DetailView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class UserProfileDetailView(DetailView):
    """ Shows User Profile """
    model = get_user_model()
    slug_field = "username"

    template_name = "user_detail.html"

class HomePageView(TemplateView):
    """ Home Page """

    template_name = "home.html"