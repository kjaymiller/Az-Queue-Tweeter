import logging
from unittest.mock import Mock

import pytest
from tweepy import API, Client

import src


def test_send_next_message_calls_client_with_text(mocker, test_queue_tweeter):
    """tests create_tweet is called when we send_next_message"""
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )
    test_queue_tweeter.send_next_message()
    src.twitter.tweepy.Client.create_tweet.assert_called_with(text="test")


def test_adding_file_triggers_media_upload(mocker, test_queue_tweeter, test_media):
    """Tests that adding file triggers media upload with those bytes"""
    media = mocker.patch("src.twitter.tweepy.API.media_upload", return_value=test_media)
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )

    def make_image_tweet(msg):
        return {"file": b"passing_in_bytes", "text": "pic!"}

    test_queue_tweeter.send_next_message(message_transformer=make_image_tweet)

    assert media.call_args.kwargs["file"] == b"passing_in_bytes"
    src.twitter.tweepy.Client.create_tweet.assert_called_with(
        text="pic!", media_ids=[123457890]
    )


def test_more_args_passed_into_send_tweet(mocker, test_queue_tweeter):
    mocker.patch(
        "src.twitter.tweepy.Client.create_tweet", return_value={"Response": 200}
    )

    def make_poll_tweet(msg):
        return {"poll_options": ["3.6", "3.7", "3.9"], "text": "when f strings?"}

    test_queue_tweeter.send_next_message(message_transformer=make_poll_tweet)

    src.twitter.tweepy.Client.create_tweet.assert_called_with(
        text="when f strings?", poll_options=["3.6", "3.7", "3.9"]
    )
