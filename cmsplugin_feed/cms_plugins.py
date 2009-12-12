import feedparser

from django.utils.translation import ugettext as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_feed.models import Feed
from cmsplugin_feed.forms import FeedForm

class FeedPlugin(CMSPluginBase):
    model = Feed
    name = _('Feed')
    form = FeedForm
    render_template = 'cmsplugin_feed/feed.html'

    def render(self, context, instance, placeholder):
        feed = feedparser.parse(instance.feed_url)
        context.update({
            'object': instance,
            'feed': feed,
            'placeholder': placeholder,
            })
        return context

plugin_pool.register_plugin(FeedPlugin)
