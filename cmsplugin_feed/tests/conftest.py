import os
import os.path

import cmsplugin_feed.cms_plugins
import pytest


def _fixtures_path():
    here = os.path.dirname(__file__)
    return os.path.join(here, "fixtures")


def _feeds_fixtures():
    fnames = os.listdir(_fixtures_path())
    files = map(lambda x: os.path.join(_fixtures_path(), x), fnames)
    return filter(os.path.isfile, files)


@pytest.fixture(scope="module", params=_feeds_fixtures())
def parsed_feed(request):
    return cmsplugin_feed.cms_plugins.fetch_parsed_feed(request.param)
