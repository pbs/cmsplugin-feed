import os.path
import cmsplugin_feed.cms_plugins


def test_image_hrefs(parsed_feed):
    assert len(parsed_feed) != 0
    entries = parsed_feed.get("entries")
    for en in entries:
        # it can be unicode
        if "image" in en:
            assert isinstance(en.get("image"), basestring)


def test_invalid_feed():
    invalid_path = os.path.join(".", "fixtures", "invalid.xml")
    feed = cmsplugin_feed.cms_plugins.fetch_parsed_feed(invalid_path)
    assert True, "No exception has been raised"
