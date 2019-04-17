from cache_memoize import cache_memoize
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from travelfootprint import analyse
from travelfootprint.analyse import Summary
from travelfootprint.insta import api
from . import forms


@cache_memoize(3600 * 24)
def _get_context(username: str):
    profile = api.get_profile(username)
    feed = api.get_feed(profile)
    trips = list(analyse.feed_to_trips(feed))
    return dict(profile=profile, trips=trips, summary=Summary(trips))


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        return dict(**super().get_context_data(), **_get_context(kwargs["username"]))


class IndexView(FormView):
    template_name = "index.html"
    form_class = forms.ProfileForm

    def get_success_url(self):
        name = self.get_form().data["name"]
        return reverse("profile", kwargs=dict(username=name))
