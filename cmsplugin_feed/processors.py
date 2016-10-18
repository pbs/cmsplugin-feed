import feedparser
from functools import wraps
from xml.sax import SAXException

from cmsplugin_feed.utils import strip_tags, get_image, prioritize_jpeg
import re


def apply(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        feed = f(*args, **kwargs)
        if feed:
            for fproc in FEED_PROCESSORS:
                feed = fproc(feed)
        return feed
    return wrapper


def remove_invalid(feed):
    entries = feed.get('entries', [])
    feed['entries'] = [e for e in entries if isinstance(e, dict)]
    return feed


def add_image_hrefs(feed):
    """ WARNING! it changes the feed arg """
    supported_image_types = ('image/jpeg', 'image/png')
    entries = feed.get('entries', [])
    for entry in entries:
        if 'image' not in entry:
            try:
                for link in entry.get('links', []):
                    try:
                        if link.get('type') in supported_image_types:
                            entry['image'] = link.get('href')
                            break
                    except AttributeError:
                        continue
            except (TypeError, AttributeError):
                pass

        image_getters = (
            lambda e: e['image'] if isinstance(e['image'], basestring) else None,
            lambda e: e['image']['href'] if e['image'] else None,
            lambda e: prioritize_jpeg(e['media_thumbnail']),
            lambda e: prioritize_jpeg(e['media_content']))

        for getter in image_getters:
            try:
                image = getter(entry)
                if image:
                    entry['image'] = image
                    break
            except (KeyError, IndexError, TypeError):
                pass
    return feed


def add_image_from_content(feed):
    entries = feed.get('entries', [])
    for entry in entries:
        if 'image' not in entry or not entry['image']:
            text = entry.get('summary', '')
            if 'content' in entry:
                try:
                    text += ''.join([e.value for e in entry['content']])
                except (TypeError, AttributeError):
                    pass
            img = get_image(text)
            if img:
                entry['image'] = img
    return feed


def fix_summary(feed):
    entries = feed.get('entries', [])
    for entry in entries:
        summary = entry.get('summary', '')
        entry['summary'] = re.sub(r"\s+", " ", strip_tags(summary))
    return feed

# keep the order of the processors
FEED_PROCESSORS = (remove_invalid, add_image_hrefs, add_image_from_content, fix_summary)


@apply
def fetch_parsed_feed(feed_url):
    """Returns the parsed feed if not malformed,"""
    feed = feedparser.parse(feed_url)
    parse_error = hasattr(feed, 'bozo_exception') and (
        isinstance(feed.bozo_exception, SAXException))
    if not feed.bozo or not parse_error:
        return feed
