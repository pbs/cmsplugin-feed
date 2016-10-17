import os.path
import time

from cmsplugin_feed.processors import FEED_PROCESSORS


def test_image_hrefs(parsed_feed):
    assert len(parsed_feed) != 0
    entries = parsed_feed.get("entries")
    for en in entries:
        # it can be unicode
        if "image" in en:
            assert isinstance(en.get("image"), basestring)


def test_invalid_feed():
    import cmsplugin_feed.cms_plugins
    invalid_path = os.path.join(".", "fixtures", "invalid.xml")
    feed = cmsplugin_feed.cms_plugins.fetch_parsed_feed(invalid_path)
    assert True, "No exception has been raised"


def test_process_real_feed():
    """
    Test that feed processors can work with real case of missing data.
    """

    feed = {'entries': [{
        'links': [{
            'href': u'http://listen.sdpb.org/post/6-pm-ct5-pm-mt-newscast-1',
            'type': u'text/html',
            'rel': u'alternate'
        }],
        'title': u'6 pm CT/5 pm MT Newscast',
        'author': u'Susan Hanson',
        'guidislink': False,
        'title_detail': {
            'base': u'http://listen.sdpb.org/news/rss.xml',
            'type': u'text/plain',
            'value': u'6 pm CT/5 pm MT Newscast',
            'language': None
        },
        'link': u'http://listen.sdpb.org/post/6-pm-ct5-pm-mt-newscast-1',
        'authors': [{'name': u'Susan Hanson'}],
        'author_detail': {'name': u'Susan Hanson'},
        'id': u'101789 as http://listen.sdpb.org',
        'published': u'Fri, 14 Oct 2016 23:14:19 +0000'
    }]}
    for processor in FEED_PROCESSORS:
        feed = processor(feed)


def test_process_missing_info():
    """
    Test that feed processors can work with missing data without raising errors.
    """
    invalid_feeds = [
        {},
        {'entries': []},
        {'entries': [2]},
        {'entries': ['3']},
    ]
    invalid_entries = [
        {},
        {'image': 1},
        {'image': 'link'},
        {'image': {}},
        {'image': {}, 'media_thumbnail': 1},
        {'image': {}, 'media_content': 2},
        {'links': {}},
        {'links': 'missing'},
        {'links': 2},
        {'links': [{}, ]},
        {'links': [{'type': 3}, ]},
        {'links': [{'type': 'image/jpeg'}, ]},
        {'content': 3},
        {'content': 'bla', 'summary': '<img>'},
    ]
    for invalid_entry in invalid_entries:
        invalid_feeds.append({'entries': [invalid_entry]},)

    for invalid_feed in invalid_feeds:
        for processor in FEED_PROCESSORS:
            invalid_feed = processor(invalid_feed)
