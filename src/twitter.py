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

        for var in (
            "access_token",
            "access_token_secret",
            "consumer_key",
            "consumer_secret",
        ):
            if locals()[var] is None:
                locals()[var] = os.environ.get(f"TWITTER_{var.upper()}")
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    @property
    def auth(self):
        return tweepy.OAuth1UserHandler(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )

    @property
    def client(self):
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )


# Create a tweet
def send_tweet(
    text: str,
    image_name: str,
    image_data: typing.Optional[bytes] = None,
    Auth: typing.Optional[Auth] = None,
    client: typing.Optional[tweepy.Client] = None,
    api: typing.Optional[tweepy.Auth] = None,
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
        client = Auth.client

    if not image_name:
        return client.create_tweet(text, **kwargs)

    if not auth:
        auth = Auth.auth

    media = api.media_upload(filename=image_name, file=image_data)
    return client.create_tweet(text=text, media_ids=[media.media_id], **kwargs)
