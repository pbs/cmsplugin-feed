import mock

from unittest import TestCase
from xml.sax import SAXException
from feedparser import CharacterEncodingOverride


class CMSPluginFeedTests(TestCase):

    def test_handle_bozo_feed(self):
        feed_url = 'url_to_bad_feed'
        with mock.patch('feedparser.parse') as mock_parse:
            mock_parse.return_value = mock.Mock(
                bozo=1, bozo_exception=SAXException('fake error'))
            from ..cms_plugins import fetch_parsed_feed
            feed = fetch_parsed_feed(feed_url)
            self.assertTrue(feed is None)

    @mock.patch('cmsplugin_feed.processors.FEED_PROCESSORS')
    def test_handle_bozo_with_bad_encoding_feed(self, mock_processors):
        mock_processors.return_value = []
        feed_url = 'url_to_good_Feed'
        with mock.patch('feedparser.parse') as mock_parse:
            mock_parse.return_value = mock.Mock(
                bozo=1, bozo_exception=CharacterEncodingOverride())
            from ..cms_plugins import fetch_parsed_feed
            feed = fetch_parsed_feed(feed_url)
            self.assertTrue(feed is not None)

    @mock.patch('cmsplugin_feed.processors.FEED_PROCESSORS')
    def test_handle_non_bozo_feed(self, mock_processors):
        mock_processors.return_value = []
        feed_url = 'url_to_good_feed'
        with mock.patch('feedparser.parse') as mock_parse:
            mock_parse.return_value = mock.Mock(bozo=0)
            from ..cms_plugins import fetch_parsed_feed
            feed = fetch_parsed_feed(feed_url)
            self.assertTrue(feed is not None)
