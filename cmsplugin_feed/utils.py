from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import os


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
    image_types = ('bmp', 'gif', 'jpeg', 'jpg', 'png', 'tif', 'tiff')

    path = urlparse(img.get('src')).path
    return os.path.splitext(path)[1][1:] in image_types

def get_image(raw_html):
    tree = BeautifulSoup(raw_html)
    for img in tree.findAll('img'):
        if not is_small(img) and is_valid_img_ext(img):
            return img.get('src') 
    return None 
