import pytest
from hymnal.catalog import HymnalLoader


def test_reload_hymnal_lib():
    HYMNAL_GITHUB_URL = 'https://github.com/goc-dev/hymnal-lib'
    HYMNAL_GITHUB_BRANCH = 'main'
    HYMNAL_HOME_DIR = './hymnal-lib--ut'
    HymnalLoader.reload_from_github( HYMNAL_GITHUB_URL, HYMNAL_GITHUB_BRANCH, HYMNAL_HOME_DIR)

    assert True