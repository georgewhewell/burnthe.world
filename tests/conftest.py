import datetime
import pytest


from travelfootprint.insta.types import BasicLocation, FeedItem, ShortCode


@pytest.fixture
def camberwell():
    return BasicLocation(
        id="488431810", name="Camberwell", slug="camberwell", has_public_page=True
    )


@pytest.fixture
def media():
    return FeedItem(
        id="1387306587937765364_11428116",
        short_code=ShortCode("BNAs_3Qlvf0"),
        display_url="https://scontent-lhr3-1.cdninstagram.com/vp/51fb6fedf03d384885ea1794ff51c7b3/5D3A5642/t51.2885-15/e35/15101770_725434790948540_3132624226578595840_n.jpg?_nc_ht=scontent-lhr3-1.cdninstagram.com",
        taken_at=datetime.datetime(2016, 11, 19, 23, 57, 34),
        location=None,
        num_likes=35,
    )
