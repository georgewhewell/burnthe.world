from datetime import timedelta
from typing import Iterator, List, ClassVar

from dataclasses import dataclass
from geopy.distance import distance

from travelfootprint.insta.api import filter_feed_for_locations
from travelfootprint.insta.types import FullLocation, FeedItem

# source: https://www.carbonindependent.org/sources_aviation.html
KG_EMISSIONS_PER_KM = 0.115


@dataclass
class Trip:
    start: FullLocation
    end: FullLocation
    evidence: FeedItem

    @property
    def distance(self):
        return distance(
            (self.start.lat, self.start.lng), (self.end.lat, self.end.lng)
        ).kilometers


class Summary:
    trips: ClassVar[List[Trip]]

    def __init__(self, trips=List[Trip]):
        self.trips = trips

    @property
    def total_distance(self) -> float:
        return sum(trip.distance for trip in self.trips)

    @property
    def carbon(self) -> float:
        return self.total_distance * KG_EMISSIONS_PER_KM

    @property
    def duration(self) -> timedelta:
        try:
            return self.trips[0].evidence.taken_at - self.trips[-1].evidence.taken_at
        except IndexError:
            return timedelta(0)


def feed_to_trips(feed: Iterator[FeedItem]) -> Iterator[Trip]:
    location_feed = filter_feed_for_locations(feed)
    try:
        to = next(location_feed)
    except StopIteration:
        return []
    for _from in location_feed:
        assert isinstance(to.location, FullLocation)
        assert isinstance(_from.location, FullLocation)
        yield Trip(to.location, _from.location, evidence=to)
        to = _from
