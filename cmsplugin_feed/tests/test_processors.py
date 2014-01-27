def test_image_hrefs(parsed_feed):
    assert len(parsed_feed) != 0
    entries = parsed_feed.get("entries")
    for en in entries:
        # it can be unicode
        if "image" in en:
            assert isinstance(en.get("image"), basestring)
