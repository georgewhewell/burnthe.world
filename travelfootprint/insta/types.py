from _pydecimal import Decimal
from datetime import datetime
from typing import Optional, List, Union

from dataclasses import dataclass


class ShortCode(str):
    pass


@dataclass(frozen=True)
class NoLocation:
    pass


@dataclass(frozen=True)
class BasicLocation:
    id: str
    name: str
    slug: str
    has_public_page: bool


@dataclass(frozen=True)
class FullLocation(BasicLocation):
    lat: Decimal
    lng: Decimal


@dataclass(frozen=True)
class FeedItem:
    id: str
    short_code: ShortCode
    display_url: str
    taken_at: datetime
    location: Optional[Union[NoLocation, BasicLocation, FullLocation]]
    num_likes: int


@dataclass(frozen=True)
class Profile:
    id: str
    username: str
    bio: str
    profile_picture: str

    is_private: bool
    feed: List[FeedItem]
