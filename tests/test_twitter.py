import pytest

from src.twitter import Auth


@pytest.mark.parametrize(
    "env_key,class_key,env_val",
    [
        ("TWITTER_ACCESS_TOKEN", "access_token", "test_access_token"),
        ("TWITTER_ACCESS_TOKEN_SECRET", "access_token_secret", "test_access_secret"),
        ("TWITTER_CONSUMER_KEY", "consumer_key", "test_consumer_key"),
        ("TWITTER_CONSUMER_SECRET", "consumer_secret", "test_consumer_secret"),
    ],
)
def test_auth_from_environ(monkeypatch, env_key, class_key, env_val):
    """Tests that you can pass in the auth credentials as environment variables."""

    monkeypatch.setenv(env_key, env_val)

    auth = Auth()
    print(vars(auth))
    assert getattr(auth, class_key) == env_val
