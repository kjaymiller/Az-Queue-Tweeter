import typing

import twitter
import storage


class QueueTweeter():

    def __init__(self, storage_auth:storage.Auth, twitter_auth:twitter.Auth):
        self.twitter_auth = twitter_auth
        self.queue = storage_auth.Client
        self.twitterv1 = twitter_auth.API
        self.twitterv2 = twitter_auth.Client

    def send_next_message(self,
        message_transformer=lambda message:{"text":message},
        delete_after:typing.Optional[bool] = True
        ):

        next_message = self.queue.receive_messages().next()

        # Turns queue message into tweet arguments
        # Must be a dict containing arguments from
        # https://docs.tweepy.org/en/stable/client.html#tweepy.Client.create_tweet
        # Or "file" (byte array) which will be uploaded w/Twitter API v1
        tweet_args = message_transformer(next_message)
        if tweet_args.get("file"):
             media = self.twitterv1.media_upload(file=tweet_args["file"])
             tweet_args["media_ids"] = [media.media_id]
             del tweet_args["file"]

        # Send the tweet
        self.twitterv2.create_tweet(**tweet_args)

        # Delete from queue if desired
        if delete_after:
            self.queue.delete_message(next_message.id, next_message.pop_receipt)

    def queue_text_message(self, message):
        self.queue_client.send_message(message)