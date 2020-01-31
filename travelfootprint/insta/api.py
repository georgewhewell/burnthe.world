import string
import hashlib
import random
import functools
from concurrent.futures import Future, as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, Iterator, Union

from cache_memoize import cache_memoize
from dataclasses import asdict
from instagram_web_api import Client

from travelfootprint.insta.types import (
    FullLocation,
    BasicLocation,
    FeedItem,
    Profile,
    ShortCode,
    NoLocation,
)

class MyClient(Client):

    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()

web_api = MyClient(auto_patch=True, drop_incompat_keys=False)
web_api.user_info = cache_memoize(3600)(web_api.user_info)
web_api.user_feed = cache_memoize(3600)(web_api.user_feed)
web_api.location_feed = cache_memoize(3600)(web_api.location_feed)
web_api.media_info2 = cache_memoize(3600)(web_api.media_info2)


def catch_keyerrors(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyError:
            raise

    return wrapped


@catch_keyerrors
def _location(basic: BasicLocation, info: Dict) -> FullLocation:
    kwargs = asdict(basic)
    kwargs.update(
        dict(
            lat=Decimal(info["data"]["location"]["lat"]),
            lng=Decimal(info["data"]["location"]["lng"]),
        )
    )
    return FullLocation(**kwargs)


@catch_keyerrors
def _location_info(info: Dict) -> BasicLocation:
    return BasicLocation(
        id=info["id"],
        name=info["name"],
        slug=info["slug"],
        has_public_page=info["has_public_page"],
    )


@catch_keyerrors
def _feed_item(item: Dict) -> FeedItem:
    node = item["node"] if "node" in item else item
    try:
        return FeedItem(
            id=node["id"],
            short_code=ShortCode(node["shortcode"]),
            display_url=node["display_url"],
            taken_at=datetime.fromtimestamp(node["taken_at_timestamp"]),
            location=_location_info(node["location"]) if node["location"] else None,
            num_likes=node["likes"]["count"]
            if "likes" in node
            else node["edge_liked_by"]["count"],
        )
    except KeyError:
        raise


@catch_keyerrors
def _profile(user_info: Dict) -> Profile:
    return Profile(
        id=user_info["id"],
        username=user_info["username"],
        bio=user_info["bio"],
        is_private=user_info["is_private"],
        feed=[
            _feed_item(edge["node"])
            for edge in user_info["edge_owner_to_timeline_media"]["edges"]
        ],
        profile_picture=user_info["profile_picture"],
    )


def get_profile(username: str) -> Profile:
    user_info = web_api.user_info2(username)
    return _profile(user_info)


def get_feed(profile: Profile) -> Iterator[FeedItem]:
    user_feed = web_api.user_feed(profile.id, count=50)
    return (_feed_item(x) for x in user_feed)


def get_full_location(location: BasicLocation) -> FullLocation:
    location_info = web_api.location_feed(location.id)
    return _location(location, location_info)


def get_media_location(media: FeedItem) -> Optional[BasicLocation]:
    media_info = web_api.media_info2(media.short_code)
    if not media_info["location"]:
        return None
    return _location_info(media_info["location"])


def populate_location(feeditem: FeedItem) -> FeedItem:
    kwargs = asdict(feeditem)
    kwargs.update(dict(location=_populate_location(feeditem.location, media=feeditem)))
    return FeedItem(**kwargs)


@functools.singledispatch
def _populate_location(
    location: Optional[Union[NoLocation, BasicLocation, FullLocation]], media: FeedItem
) -> Union[NoLocation, BasicLocation, FullLocation]:
    raise NotImplementedError()


@_populate_location.register
def _get_location_none(location: NoLocation, media: FeedItem):
    return NoLocation()


@_populate_location.register
def _get_location_notfound(location: None, media: FeedItem):
    media_location = get_media_location(media)
    if media_location is None:
        return NoLocation()
    return get_full_location(media_location)


@_populate_location.register
def _get_location_basic(location: BasicLocation, *_):
    return get_full_location(location)


@_populate_location.register
def _get_location_full(location: NoLocation, *_):
    return location


def location_populated_feed(feed: Iterator[FeedItem]) -> Iterator[Future]:
    with ThreadPoolExecutor(max_workers=8) as executor:
        yield from as_completed(executor.submit(populate_location, f) for f in feed)


def filter_feed_for_locations(feed: Iterator[FeedItem]) -> Iterator[FeedItem]:
    for future in location_populated_feed(feed):
        try:
            result = future.result()
        except Exception as exc:
            print("generated an exception: %s" % (exc))
        else:
            if isinstance(result.location, FullLocation):
                yield result
