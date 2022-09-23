import logging
from unittest.mock import Mock

import pytest
from tweepy import API, Client

import src
from src.twitter import Auth, send_tweet


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


def test_Auth_has_api(test_auth):
    """assert that Auth has an api property. MyPy will enforce type"""

    assert test_auth.API


def test_Auth_has_client(test_auth):
    """assert that Auth has an client property. MyPy will enforce type"""

    assert test_auth.Client


def test_send_tweet_pulls_client_from_Auth(mocker, test_auth):
    """tests if Auth is passed and client is not client is pulled from Auth"""
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )
    send_tweet("test", auth=test_auth)
    src.twitter.tweepy.Client.create_tweet.assert_called_with("test")


def test_send_tweet_accepts_custom_client(mocker, test_auth):
    """Tests that you can pass in a custom client"""
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )

    send_tweet("test", client=test_auth.Client)
    src.twitter.tweepy.Client.create_tweet.assert_called_with("test")


@pytest.mark.skip("Not Sure how to Test")
def test_send_tweet_accepts_custom_client_over_Auth(mocker, test_auth):
    """Tests that a custom_client is used and not the Auth object"""
    pass


def test_passing_image_name_triggers_media_upload(mocker, test_auth, test_media):
    """Tests that adding filename triggers media upload with that filename"""
    media = mocker.patch("src.twitter.tweepy.API.media_upload", return_value=test_media)
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )

    send_tweet("test", image_name="filepath", auth=test_auth)

    assert media.call_args.kwargs["filename"] == "filename"


def test_passing_image_name_triggers_media_upload(mocker, test_auth, test_media):
    """Tests that adding filename triggers media upload with that filename"""
    media = mocker.patch("src.twitter.tweepy.API.media_upload", return_value=test_media)
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )

    send_tweet(
        "test", image_name="filepath", image_data=b"passing_in_bytes", auth=test_auth
    )

    assert media.call_args.kwargs["file"] == b"passing_in_bytes"


@pytest.mark.skip("#TODO: Build Test")
def test_kwargs_passed_into_send_tweet():
    pass


def test_api_from_Auth(mocker, test_auth, test_media):
    """tests if Auth is passed and api is not api is pulled from Auth"""
    mocker.patch("src.twitter.tweepy.API.media_upload", return_value=test_media)
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )
    send_tweet("test", image_name="filepath", auth=test_auth)

    assert src.twitter.tweepy.API.media_upload.called_once()


def test_send_tweet_from_custom_api(mocker, test_auth, test_media):
    """tests if Auth is passed and api is not api is pulled from Auth"""
    mocker.patch("src.twitter.tweepy.API.media_upload", return_value=test_media)
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )
    send_tweet(
        "test", image_name="filepath", api=test_auth.API, client=test_auth.Client
    )

    assert src.twitter.tweepy.API.media_upload.called_once()
