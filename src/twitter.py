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
    def api(self) -> tweepy.OAuth1UserHandler:
        return tweepy.OAuth1UserHandler(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )

    @property
    def client(self) -> tweepy.Client:
        return tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )


# Create a tweet
def send_tweet(
    text: str,
    image_name: typing.Optional[str] = None,
    image_data: typing.Optional[bytes] = None,
    auth: typing.Optional[Auth] = None,
    client: typing.Optional[tweepy.Client] = None,
    api: typing.Optional[tweepy.API] = None,
    **kwargs,
):
    """
    Send a tweet with an image.

    **kwargs are passed to [tweepy.Client.send_tweet](https://docs.tweepy.org/en/latest/api.html#tweepy.Client.send_tweet)

    Note:
        if image_data is None, then it will try to open the image from the `image_name` path.

    Note:
        if api and client are None, then it will look for `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET`, `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET` in the environment variables.
    """

    if not client:
        client = auth.client

    if not image_name:
        return client.create_tweet(text, **kwargs)

    if not auth:
        auth = Auth.auth
    api = tweepy.API(auth)
    media = api.media_upload(filename=image_name, file=image_data)
    return client.create_tweet(text=text, media_ids=[media.media_id], **kwargs)
