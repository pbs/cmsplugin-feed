from nose.tools import assert_equal
import feedparser
import pickle

URL_FOR_BAD_FEED = 'http://www.pbs.org/newshour/rss/'

def test_pickleble():
    feed = feedparser.parse(URL_FOR_BAD_FEED)
    dump = pickle.dumps(feed)
