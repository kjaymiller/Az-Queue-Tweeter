import logging
import os
import typing

import tweepy  # type:ignore[import]


class Auth:
    def __init__(
        self,
        *,
        access_token: typing.Optional[str] = None,
        access_token_secret: typing.Optional[str] = None,
        consumer_key: typing.Optional[str] = None,
        consumer_secret: typing.Optional[str] = None,
    ):

        auth_keys = {
            "access_token": access_token,
            "access_token_secret": access_token_secret,
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
        }

        for key, value in auth_keys.items():
            if value is None:
                auth_keys[key] = os.environ.get(f"TWITTER_{key.upper()}")

                if auth_keys[key] is None:
                    logging.warning(
                        f"{key} not passed or in environment variables. \
                        Manually set {key} prior to using auth."
                    )

        self.access_token = auth_keys["access_token"]
        self.access_token_secret = auth_keys["access_token_secret"]
        self.consumer_key = auth_keys["consumer_key"]
        self.consumer_secret = auth_keys["consumer_secret"]

    @property
    def API(self) -> tweepy.OAuth1UserHandler:
        auth = tweepy.OAuth1UserHandler(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )
        return tweepy.API(auth)

    @property
    def Client(self) -> tweepy.Client:
        return tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )
