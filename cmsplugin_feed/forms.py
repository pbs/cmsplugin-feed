from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from cmsplugin_feed.models import Feed
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import feedparser


class StripURLWidget(admin.widgets.AdminURLFieldWidget):

    def value_from_datadict(self, data, files, name):
        value = super(StripURLWidget, self).value_from_datadict(
            data, files, name)
        if hasattr(value, 'strip'):
            return value.strip()
        return value


class FeedForm(ModelForm):

    class Meta:
        model = Feed
        widgets = {
            'feed_url': StripURLWidget
        }
        exclude = ()

    def clean_feed_url(self):
        feed_url = self.cleaned_data['feed_url']
        feed = feedparser.parse(feed_url)
        if not feed or not hasattr(feed, 'version') or not feed.version:
            raise ValidationError(_("The feed doesn't have a valid RSS format"))
        return self.cleaned_data['feed_url']
