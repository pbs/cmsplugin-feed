import re
from BeautifulSoup import BeautifulSoup
from textblob import TextBlob
from urlparse import urlparse
from HTMLParser import HTMLParser
from itertools import chain
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


def to_string(node):
    ret = re.sub(u"\s+",strip_tags(unicode(node))," ").strip()
    return ret


def is_valid_img_ext(path):
    image_types = ('bmp', 'gif', 'jpeg', 'jpg', 'png', 'tif', 'tiff')
    return  os.path.splitext(path)[1][1:] in image_types

def has_verb(line):
    """ Iterate over the words in the line, tag each one if it is a verb or a 
    noun or something else. Return True if there is at least a verb """
    blob = TextBlob(line)
    for word, part_of_speech_tag in blob.tags:
        if part_of_speech_tag[:2] == "VB":
            return True
    return False

def get_credit(line):
    """ Extract a substring as large as possible that starts with one of the 
    hardcoded keywords. This is used to shorten the image credit description """
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
    credit = get_credit(line)
    if has_verb(credit):
        return "", ""
    return line, credit

def get_valid_image_node(summary):
    tree = BeautifulSoup(summary)
    for node in tree.findAll('img'):
        if is_valid_img_ext(urlparse(node.get('src')).path):
            return node
    return None

def get_image_line_credit(summary): #return whole image, parsing might have to be done
    img = get_valid_image_node(summary)
    if img:
        node = img

        # traverse following siblings,
        # then go up one level until a string is found
        while (not (to_string(node)) and (node.nextSibling or node.parent)):
            while not (to_string(node)) and node.nextSibling:
                node = node.nextSibling
            if not (to_string(node)) and node.parent:
                node = node.parent
        text = to_string(node)

        if not text:
            return (None, "", "")

        line, credit = filter_sentence(text)
        credit = credit.lstrip(" ;")
        return (img, line, credit)
    return (None, "", "")


def get_image_summary_credit(summary):
    image, line, credit = get_image_line_credit(summary)
    cleaned_summary = to_string(summary).replace(line, "")
    return image, cleaned_summary , credit


#def get_image(raw_html):
#    tree = BeautifulSoup(raw_html)
#    img = tree.find('img')
#    return img.get('src') if img else None
