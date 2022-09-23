from dataclasses import dataclass

import pytest

from src.twitter import Auth


@pytest.fixture(scope="session")
def test_auth():
    return Auth(
        consumer_key="Foo",
        consumer_secret="Bar",
        access_token="Biz",
        access_token_secret="Baz",
    )


@dataclass
class Media:
    media_id: int
    media_id_string: str


@pytest.fixture()
def test_media():
    return Media(123457890, "123457890")
