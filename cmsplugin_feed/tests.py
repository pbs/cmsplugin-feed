import mock

from nose.tools import assert_true
from xml.sax import SAXException
from feedparser import CharacterEncodingOverride
from .cms_plugins import fetch_parsed_feed


def test_handle_bozo_feed():
    feed_url = 'url_to_bad_feed'
    with mock.patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = mock.Mock(
            bozo=1, bozo_exception=SAXException('fake error'))
        feed = fetch_parsed_feed(feed_url)
        assert_true(feed is None)


def test_handle_bozo_with_bad_encoding_feed():
    feed_url = 'url_to_good_Feed'
    with mock.patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = mock.Mock(
            bozo=1, bozo_exception=CharacterEncodingOverride())
        feed = fetch_parsed_feed(feed_url)
        assert_true(feed is not None)


def test_handle_non_bozo_feed():
    feed_url = 'url_to_good_feed'
    with mock.patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = mock.Mock(bozo=0)
        feed = fetch_parsed_feed(feed_url)
        assert_true(feed is not None)
