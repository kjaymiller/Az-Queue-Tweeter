import logging
from unittest.mock import Mock

import pytest
from tweepy import API, Client

import azqueuetweeter
from azqueuetweeter.twitter import Auth


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
    assert getattr(auth, class_key) == env_val


@pytest.mark.parametrize(
    "env_key,env_param",
    [
        ("TWITTER_ACCESS_TOKEN", "access_token"),
        ("TWITTER_ACCESS_TOKEN_SECRET", "access_token_secret"),
        ("TWITTER_CONSUMER_KEY", "consumer_key"),
        ("TWITTER_CONSUMER_SECRET", "consumer_secret"),
    ],
)
def test_empty_auth_warning_raised(caplog, monkeypatch, env_key, env_param):
    """Tests that a warning is raised if a value is not found"""

    caplog.set_level(logging.WARNING)
    monkeypatch.delenv(env_key, raising=False)

    auth = Auth()
    assert any([env_param in x.message for x in caplog.records])


def test_Auth_has_api(test_twitter_auth):
    """assert that Auth has an api property. MyPy will enforce type"""

    assert test_twitter_auth.API


def test_Auth_has_client(test_twitter_auth):
    """assert that Auth has an client property. MyPy will enforce type"""

    assert test_twitter_auth.Client
