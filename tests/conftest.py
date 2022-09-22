import pytest

from src.twitter import Auth


@pytest.fixture
def test_auth():
    return Auth(
        consumer_key="Foo",
        consumer_secret="Bar",
        access_token="Biz",
        access_token_secret="Baz",
    )
