from travelfootprint.analyse import feed_to_trips
from travelfootprint.insta.api import get_profile, get_feed


def test_feed_to_trips():
    profile = get_profile("georgewhewell")
    feed = get_feed(profile)
    first = next(feed_to_trips(feed))
    assert first.distance > 1000
