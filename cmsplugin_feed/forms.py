from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from cmsplugin_feed.models import Feed


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
