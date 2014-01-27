from functools import wraps


def apply(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        feed = f(*args, **kwargs)
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
            for link in entry.links:
                if link['type'] in supported_image_types:
                    entry['image'] = link['href']
                break
        elif isinstance(entry['image'], dict) and 'href' in entry['image']:
            entry['image'] = entry['image'].get('href')
    return feed


FEED_PROCESSORS = (add_image_hrefs,)


