from functools import wraps
from cmsplugin_feed.utils import strip_tags
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


def add_image_hrefs(feed):
    """ WARNING! it changes the feed arg """
    supported_image_types = ('image/jpeg', 'image/png')
    entries = feed['entries']
    for entry in entries:
        if 'image' not in entry:
            for link in entry.get('links', []):
                if link.get('type') in supported_image_types:
                    entry['image'] = link.get('href')
                    break
        elif isinstance(entry['image'], dict) and 'href' in entry['image']:
            entry['image'] = entry['image'].get('href')
    return feed


def fix_summary(feed):
    entries = feed['entries']
    for entry in entries:
        entry['summary'] = re.sub(u"\s+", " ", strip_tags(entry['summary']))
    return feed


FEED_PROCESSORS = (add_image_hrefs, fix_summary)
