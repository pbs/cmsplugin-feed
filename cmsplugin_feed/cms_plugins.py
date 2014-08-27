import feedparser
from xml.sax import SAXException

from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_feed.models import Feed
from cmsplugin_feed.forms import FeedForm
from cmsplugin_feed.settings import CMSPLUGIN_FEED_CACHE_TIMEOUT

import cmsplugin_feed.processors
from HTMLParser import HTMLParser
import BeautifulSoup


def get_cached_or_latest_feed(instance):
    """Get the feed from cache if it exists else fetch it."""
    feed_key = "feed_%s" % instance.id

    def cached_feed():
        return cache.get(feed_key)

    def updated_feed():
        valid_parsed_feed = fetch_parsed_feed(instance.feed_url)
        cache.set(feed_key, valid_parsed_feed, CMSPLUGIN_FEED_CACHE_TIMEOUT)
        return valid_parsed_feed
    return cached_feed() or updated_feed()


@cmsplugin_feed.processors.apply
def fetch_parsed_feed(feed_url):
    """Returns the parsed feed if not malformed,"""
    feed = feedparser.parse(feed_url)
    parse_error = hasattr(feed, 'bozo_exception') and (
        isinstance(feed.bozo_exception, SAXException))
    if not feed.bozo or not parse_error:
        return feed


class FeedPlugin(CMSPluginBase):
    model = Feed
    name = _('RSS Feed')
    form = FeedForm
    render_template = 'cmsplugin_feed/feed.html'

    def render(self, context, instance, placeholder):
        feed = get_cached_or_latest_feed(instance)
        if not feed:
            entries = []
            is_paginated = False
        else:
            if instance.paginate_by:
                is_paginated = True
                request = context['request']
                feed_page_param = "feed_%s_page" % str(instance.id)
                feed_paginator = Paginator(
                    feed['entries'], instance.paginate_by)
                # Make sure page request is an int. If not, deliver first page.
                try:
                    page = int(request.GET.get(feed_page_param, '1'))
                except ValueError:
                    page = 1
                # If page request (9999) is out of range, deliver last page of
                # results.
                try:
                    entries = feed_paginator.page(page)
                except (EmptyPage, InvalidPage):
                    entries = feed_paginator.page(feed_paginator.num_pages)
            else:
                entries = feed["entries"]
                is_paginated = False

        for e in entries:
            e['image'] = get_image(e['summary'])
            e['summary'] = strip_tags(e['summary'])

        context.update({
            'instance': instance,
            'feed_entries': entries,
            'is_paginated': is_paginated,
            'placeholder': placeholder,
        })
        return context


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_image(raw_html):
    tree = BeautifulSoup.BeautifulSoup(raw_html)
    img = tree.find('img')
    return img.get('src') if img else None

plugin_pool.register_plugin(FeedPlugin)
