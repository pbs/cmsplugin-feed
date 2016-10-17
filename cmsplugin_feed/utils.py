from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import os
from cmsplugin_feed.settings import IMAGE_TYPES
from collections import defaultdict
import re


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


def is_small(img):
    for key, value in img.attrs:
        if key in (u'height', u'width') and value == u'1':
            return True
    return False


def is_valid_img_ext(img):
    try:
        path = urlparse(img.get('src')).path
    except AttributeError:
        return False
    return os.path.splitext(path)[1][1:] in IMAGE_TYPES


def get_image(raw_html):
    tree = BeautifulSoup(raw_html)
    for img in tree.findAll('img'):
        if not is_small(img) and is_valid_img_ext(img):
            return img.get('src')
    return None

def prioritize_jpeg(img_list):
    first_of_every_kind = {}
    for img in img_list:
        if 'url' in img:
            ext = os.path.splitext(img['url'])[1][1:]
            first_of_every_kind.setdefault(ext, img['url'])

    if 'gif' in first_of_every_kind:
        ampersand = '&#38;'
        first_of_every_kind['gif'] =  re.sub(
            '&', ampersand, first_of_every_kind['gif'])

    for ext in IMAGE_TYPES:
        if ext in first_of_every_kind:
            return first_of_every_kind[ext]
    return None
