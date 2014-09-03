from django.forms.models import ModelForm
from django import forms

from cmsplugin_feed.models import Feed
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import feedparser


class FeedForm(ModelForm):
    class Meta:
        model = Feed

    def clean_feed_url(self):
        feed_url = self.cleaned_data['feed_url']
        feed = feedparser.parse(feed_url)
        if not feed.version:
            raise ValidationError(_("The feed doesn't have a valid RSS format"))
        return self.cleaned_data
