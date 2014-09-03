from functools import wraps
from cmsplugin_feed.utils import get_image_summary_credit


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


def fix_content(feed):
    entries = feed['entries']
    for entry in entries:
        image, summary, credit = get_image_summary_credit(entry['summary'])
        entry['summary'] = summary
        entry['image_from_summary'] = image
        entry['credit_from_summary'] = credit
    return feed

def set_image(feed):
    entries = feed['entries']
    for entry in entries:
        if not 'image' in entry:
            # insert heuristic to choose image here, when there will be multiple images to choose from
            if entry['image_from_summary']:
                entry['image'] = entry['image_from_summary'].get('src')
                entry['credit'] = entry['credit_from_summary']
    return feed

# leave the processor order as it is!!!
FEED_PROCESSORS = (add_image_hrefs, fix_content, set_image)
