from decimal import Decimal
from unittest.mock import ANY

from dataclasses import asdict

from travelfootprint.insta.api import (
    get_profile,
    get_feed,
    get_media_location,
    get_full_location,
    filter_feed_for_locations,
)
from travelfootprint.insta.types import FeedItem, Profile, FullLocation


def test_can_get_profile():
    profile = get_profile("georgewhewell")
    assert profile == Profile(
        id="11428116",
        username="georgewhewell",
        bio=ANY,
        profile_picture=ANY,
        is_private=False,
        feed=ANY,
    )


def test_get_feed():
    profile = get_profile("georgewhewell")
    feed = get_feed(profile)
    first = next(feed)
    assert first.id
    assert isinstance(first, FeedItem)


def test_get_media_location(media, camberwell):
    location = get_media_location(media)
    assert location == camberwell


def test_get_location_info(camberwell):
    location = get_full_location(camberwell)
    assert location == FullLocation(
        **asdict(camberwell), lat=Decimal(51.4736), lng=Decimal(-0.0912)
    )


def test_get_all_locations():
    profile = get_profile("georgewhewell")
    feed = get_feed(profile)
    for item in filter_feed_for_locations(feed):
        assert item.location.lat
        break
    else:
        assert False
