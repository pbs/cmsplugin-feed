import feedparser

from django.utils.translation import ugettext as _
from django.core.cache import cache

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_feed.models import Feed
from cmsplugin_feed.forms import FeedForm

def get_cached_feed(instance):
    """
    get the feed from cache if it exists else fetch it.
    """
    if not cache.has_key("feed_%s" %instance.id):
        feed = feedparser.parse(instance.feed_url)
        cache.set("feed_%s" %instance.id, feed, 100)
    return cache.get("feed_%s" %instance.id)

class FeedPlugin(CMSPluginBase):
    model = Feed
    name = _('Feed')
    form = FeedForm
    render_template = 'cmsplugin_feed/feed.html'

    def render(self, context, instance, placeholder):
        feed = get_cached_feed(instance)
        context.update({
            'object': instance,
            'feed': feed,
            'placeholder': placeholder,
            })
        return context

plugin_pool.register_plugin(FeedPlugin)
