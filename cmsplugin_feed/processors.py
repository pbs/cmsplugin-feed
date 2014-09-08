from functools import wraps
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
        if ('image' in entry
                and isinstance(entry['image'], dict)
                and 'href' in entry['image']):
            entry['image'] = entry['image'].get('href')

        elif ('media_thumbnail' in entry
                and entry['media_thumbnail']
                and isinstance(entry['media_thumbnail'], list)
                and 'url' in entry['media_thumbnail'][0]):
            entry['image'] = entry['media_thumbnail'][0]['url']

        elif ('media_content' in entry
                and entry['media_content']
                and isinstance(entry['media_content'], list)):
            entry['image'] = prioritize_jpeg(entry['media_content'])
    return feed


def add_image_from_content(feed):
    entries = feed['entries']
    for entry in entries:
        if 'image' not in entry or not entry['image']:
            text = entry['summary']
            if 'content' in entry:
                text += ''.join([e.value for e in entry['content']])
            img = get_image(text)
            if img:
                entry['image'] = img
    return feed


def fix_summary(feed):
    entries = feed['entries']
    for entry in entries:
        entry['summary'] = re.sub(u"\s+", " ", strip_tags(entry['summary']))
    return feed

# keep the order of the processors
FEED_PROCESSORS = (add_image_hrefs, add_image_from_content, fix_summary)
