import re
from BeautifulSoup import BeautifulSoup
from textblob import TextBlob
from urlparse import urlparse
from HTMLParser import HTMLParser
from itertools import chain


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


def mini(x):
    if not x:
        return ""
    x = re.sub("\n+", " ", x)
    x = re.sub("\r+", " ", x)
    x = filter(lambda x: x not in "\n\t\r", x)
    x = re.sub(" +", " ", x).strip()
    return x


def toString(branch):
    ret = mini(strip_tags(unicode(branch)))
    return ret


def valid_img_ext(path):
    image_types = ['bpm', 'gif', 'jpeg', 'jpg', 'png', 'tif', 'tiff']
    path_ending = path[-4:].lower()
    for img_type in image_types:
        if path_ending.endswith(img_type):
            return True
    return False

def has_verb(line):
    blob = TextBlob(line)
    for word, part_of_speech_tag in blob.tags:
        if part_of_speech_tag[:2] == "VB":
            return True
    return False

def slice_from_keywords(line):
    line_lower = line.lower()
    keywords = ["via ", "illustrated ", "photo ",
                "image credit:", "credit:", "image "]
    minimum = len(line)
    for keyword in keywords:
        pos = line_lower.find(keyword)
        if pos != -1 and pos < minimum:
            minimum = pos

    if minimum != len(line):
        return line[minimum:]
    return line

def filter_sentence(line):
    credit = slice_from_keywords(line)
    if has_verb(credit):
        return "", ""
    return line, credit

def get_valid_image_node(summary):
    tree = BeautifulSoup(summary)
    for node in tree.findAll('img'):
        if valid_img_ext(urlparse(node.get('src')).path):
            return node
    return None

def get_line_credit(summary):
    img = get_valid_image_node(summary)
    if img:
        node = img

        # traverse following siblings,
        # then go up one level until a string is found
        while (not (toString(node)) and (node.nextSibling or node.parent)):
            while not (toString(node)) and node.nextSibling:
                node = node.nextSibling
            if not (toString(node)) and node.parent:
                node = node.parent
        stuff = toString(node)

        if not stuff:
            return ("", "")

        line, credit = filter_sentence(stuff)
        credit = credit.lstrip(" ;")
        return (line, credit)
    return ("", "")


def get_credit_summary(summary):
    line, credit = get_line_credit(summary)
    return credit, toString(summary).replace(line, "")


def get_image(raw_html):
    tree = BeautifulSoup(raw_html)
    img = tree.find('img')
    return img.get('src') if img else None
